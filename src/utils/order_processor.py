import logging
from pathlib import Path
from tqdm import tqdm
from src.utils import get_discount_by_total, calculate_order_total

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("order_processing.log", encoding='utf-8'),  # записываем логи в файл
        logging.StreamHandler()  # выводи лог в консоль
    ]
)
logger = logging.getLogger(__name__)


def process_order_file(input_file_path: str, output_file_path: str):
    """
    Обработка файла заказов.
    :param input_file_path: Путь до входного файла.
    :param output_file_path: Путь до выходного файла.
    """
    # Проверка расширения
    output_path = Path(output_file_path)
    if output_path.suffix != '.txt':
        output_path = output_path.with_suffix('.txt')
    output_file_path = str(output_path)

    try:
        orders_from_file = load_orders_from_file(input_file_path)

        if orders_from_file is None:
            logger.error("Не удалось загрузить заказы.")
            return

        processed_orders = process_orders(orders_from_file)
        order_stats = analyze_orders(processed_orders)

        by_status = ', '.join([f'{k}: {v}' for k, v in order_stats['by_status'].items()])
        sample_log = (
            f"Обработано заказов: {order_stats['total_orders']}\n"
            f"Общая сумма: {order_stats['total_sum']} руб.\n"
            f"По статусам: {by_status}\n"
            f"Уникальных пользователей: {len(order_stats['unique_users'])}\n"
        )

        with open(output_file_path, "a", encoding='utf-8') as f:
            f.write(sample_log)
        logger.info(f"Отчёт успешно сохранён в {output_file_path}")
    except Exception as e:
        logger.error(f"Не удалось записать файл отчёта: {e}")


def load_orders_from_file(file_path: str) -> list[str] | None:
    """
    Загружает данные заказов из файла.
    :param file_path: Путь к файлу.
    :return: Возвращает список заказов или None при ошибке.
    """
    logger.info(f"Загрузка заказов из файла: {file_path}")
    try:
        with open(Path(file_path), "r", encoding='utf-8') as f:
            lines = f.readlines()
        orders = [line.strip() for line in lines if line.strip()]
        logger.info(f"Загружено {len(orders)} строк из файла.")
        return orders
    except FileNotFoundError:
        logger.error(f"Файл по пути {file_path} отсутствует.")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении файла: {e}")
    return None


def process_orders(orders_data: list[str]) -> list[dict]:
    """
    Обработка, валидация и подготовка списка словарей для записи.
    :param orders_data: Список строк с данными о товарах.
    :return: Список словарей готовых к записи.
    """
    orders: list[dict] = []

    if not orders_data:
        logger.warning("Список данных о заказах пуст.")
        return orders

    for order in tqdm(orders_data, desc="Обработка заказов..."):
        parts = order.strip().split(":")

        if len(parts) != 4 or any(not p.strip() for p in parts):
            logger.error(f"Неверный формат или пустые поля: {order}")
            continue

        try:
            order_id, total_str, status, user = parts
            total = float(total_str)
            discount_rate = get_discount_by_total(total)
            final_price = calculate_order_total(total, discount_rate=discount_rate)

            order_entry = {
                "order_id": order_id,
                "total": final_price,
                "status": status,
                "user": user,
            }
            orders.append(order_entry)
        except ValueError as e:
            logger.error(f"Ошибка преобразования данных в строке: {order}. Ошибка: {e}")
            continue
        except Exception as ex:
            logger.error(f"Неожиданная ошибка при обработке строки: {order}. Ошибка: {ex}")
            continue

    logger.info(f"Обработано записей: {len(orders)}, пропущено: {len(orders_data) - len(orders)}")
    return orders


def analyze_orders(processed_orders: list[dict]) -> dict:
    """
    Анализирует список заказов и формирует отчет.
    :param processed_orders: Список обрабатанных заказов.
    :return: Словарь со статистикой.
    """
    stats: dict = {
        "total_orders": 0,
        "total_sum": 0.0,
        "by_status": {},
        "unique_users": set()
    }

    if not processed_orders:
        logger.warning("Список заказов пуст.")
        return stats

    for order in tqdm(processed_orders, desc="Сбор статистики..."):
        try:
            stats["total_sum"] += float(order["total"])
            status = order["status"]
            user = order["user"]
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            stats["unique_users"].add(user)
        except (TypeError, KeyError, ValueError) as e:
            logger.error(f"Ошибка в данных заказа: {order}. Ошибка: {e}")
            continue

    stats["total_orders"] = len(processed_orders)
    stats["unique_users"] = list(stats["unique_users"])

    return stats
