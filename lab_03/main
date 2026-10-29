from data_structures import Queue, LinkedList, Stack


def load_requests(path):
    def field(parts, i):
        return parts[i] if i < len(parts) else ""

    requests = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]

            try:
                number = int(field(parts, 0))
            except ValueError:
                number = -1

            requests.append({
                "номер": number,
                "клиент": field(parts, 1),
                "тип": field(parts, 2),
                "категория": field(parts, 3),
                "приоритет": field(parts, 4),
                "_line": line_no,
                "_fields": len(parts),
            })
    return requests


def process_requests(raw_requests):
    used_ids = set()
    errors = []
    types = {"ремонт", "консультация", "установка"}
    priorities = {"обычная", "срочная"}

    normal_q = Queue()
    urgent_q = Queue()
    requests_by_id = {}
    stack = Stack()
    correct_count = 0

    for req in raw_requests:
        num = req["номер"]
        if req["_fields"] != 5:
            errors.append(f"Строка {req['_line']}: неверное количество полей.")
            continue
        if num <= 0:
            errors.append(f"Строка {req['_line']}: неверный формат номера заявки.")
            continue
        if num in used_ids:
            errors.append(f"Строка {req['_line']}: повторяющийся номер заявки {num}.")
            continue
        if req["клиент"] == "":
            errors.append(f"Строка {req['_line']}: пустое обязательное поле (клиент).")
            continue
        if req["тип"].lower() not in types:
            errors.append(f"Строка {req['_line']}: неизвестный тип заявки: '{req['тип']}'.")
            continue
        if req["категория"] == "":
            errors.append(f"Строка {req['_line']}: пустое обязательное поле (категория).")
            continue
        if req["приоритет"].lower() not in priorities:
            errors.append(f"Строка {req['_line']}: неизвестный приоритет: '{req['приоритет']}'.")
            continue

        req["тип"] = req["тип"].lower()
        req["приоритет"] = req["приоритет"].lower()
        correct_count += 1
        req["_arrival_order"] = correct_count

        used_ids.add(num)
        requests_by_id[num] = req
        stack.push(num)

        if req["приоритет"] == "срочная":
            urgent_q.enqueue(req)
        else:
            normal_q.enqueue(req)

    return normal_q, urgent_q, requests_by_id, stack, errors, correct_count


def serve_request(urgent_q, normal_q, history, stack, service_counter):
    if len(urgent_q) > 0:
        req = urgent_q.dequeue()
    elif len(normal_q) > 0:
        req = normal_q.dequeue()
    else:
        return None, service_counter

    stack.pop()
    service_counter += 1
    req["_service_order"] = service_counter
    history.add_in_tail(req)
    return req, service_counter


def cancel_request(urgent_q, normal_q, request_id):
    if urgent_q.remove_value(request_id):
        return True
    if normal_q.remove_value(request_id):
        return True
    return False


def cancel_last_accepted(stack, urgent_q, normal_q):
    if len(stack) == 0:
        return None
    request_id = stack.pop()
    if urgent_q.remove_value(request_id):
        return request_id
    if normal_q.remove_value(request_id):
        return request_id
    return request_id


def get_statistics(history):
    stats = {
        "ремонт": {"count": 0, "urgent": 0, "total_wait": 0, "max_wait": 0},
        "консультация": {"count": 0, "urgent": 0, "total_wait": 0, "max_wait": 0},
        "установка": {"count": 0, "urgent": 0, "total_wait": 0, "max_wait": 0},
    }

    for req in history.to_list():
        t = req["тип"]
        wait_time = req["_service_order"] - req["_arrival_order"]

        stats[t]["count"] += 1
        if req["приоритет"] == "срочная":
            stats[t]["urgent"] += 1

        stats[t]["total_wait"] += wait_time
        if wait_time > stats[t]["max_wait"]:
            stats[t]["max_wait"] = wait_time

    result = []
    for t, data in stats.items():
        if data["count"] > 0:
            avg_wait = round(data["total_wait"] / data["count"], 2)
        else:
            avg_wait = 0
        result.append({
            "тип": t,
            "количество": data["count"],
            "срочных": data["urgent"],
            "среднее_ожидание": avg_wait,
            "макс_ожидание": data["max_wait"]
        })
    return result


def get_unique_categories(raw_requests):
    categories = set()
    for req in raw_requests:
        if isinstance(req.get("категория"), str) and req["категория"] != "":
            categories.add(req["категория"])
    return sorted(categories)


def save_report(filename, correct_count, errors, categories, stats, history):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Количество корректных записей: {correct_count}\n")
        f.write(f"Количество некорректных записей: {len(errors)}\n\n")
        f.write("Уникальные категории:\n")
        for cat in categories:
            f.write(f"- {cat}\n")
        f.write("\nСтатистика по типам заявок:\n")
        for s in stats:
            f.write(f"{s['тип']}: всего={s['количество']}, срочных={s['срочных']}, "
                    f"среднее ожидание={s['среднее_ожидание']}, макс. ожидание={s['макс_ожидание']}\n")
        f.write("\nСписок обслуженных заявок:\n")
        for req in history.to_list():
            f.write(f"{req['номер']}; {req['клиент']}; {req['тип']}; {req['категория']}; {req['приоритет']}\n")
        f.write("\nСписок ошибок входных данных:\n")
        for err in errors:
            f.write(f"{err}\n")


def print_queue(q, title):
    print(f"--- {title} ---")
    if len(q) == 0:
        print("(пусто)")
    else:
        for req in q.to_list():
            print(f"{req['номер']} | {req['клиент']} | {req['тип']} | {req['категория']} | {req['приоритет']}")


def print_history(history):
    print("--- История обслуживания ---")
    if len(history) == 0:
        print("(пусто)")
    else:
        for req in history.to_list():
            print(f"{req['номер']} | {req['клиент']} | {req['тип']} | {req['категория']} | {req['приоритет']}")


def main():
    try:
        raw_requests = load_requests("requests.txt")
    except FileNotFoundError:
        print("Ошибка: входной файл не найден.")
        return

    normal_q, urgent_q, requests_by_id, stack, errors, correct_count = process_requests(raw_requests)
    history = LinkedList()
    service_counter = 0
    categories = get_unique_categories(raw_requests)

    while True:
        print("\n1. Показать заявки в очередях")
        print("2. Обслужить заявку")
        print("3. Отменить заявку по номеру")
        print("4. Отменить последнюю принятую заявку")
        print("5. Показать историю обслуживания")
        print("6. Развернуть историю")
        print("7. Показать статистику")
        print("8. Найти заявку по номеру")
        print("9. Сохранить отчёт")
        print("0. Завершить программу")

        try:
            choice = input("Выберите пункт: ").strip()
        except EOFError:
            break

        if choice == "0":
            break
        elif choice == "1":
            print_queue(urgent_q, "Срочные заявки")
            print_queue(normal_q, "Обычные заявки")
        elif choice == "2":
            req, service_counter = serve_request(urgent_q, normal_q, history, stack, service_counter)
            if req is None:
                print("Обе очереди пусты.")
            else:
                print(f"Обслужена заявка {req['номер']} ({req['клиент']})")
        elif choice == "3":
            try:
                req_id = int(input("Введите номер заявки для отмены: ").strip())
                if cancel_request(urgent_q, normal_q, req_id):
                    print(f"Заявка {req_id} отменена.")
                else:
                    print(f"Заявка {req_id} не найдена.")
            except ValueError:
                print("Ошибка: введите целое число.")
        elif choice == "4":
            if len(stack) == 0:
                print("Нет принятых заявок для отмены.")
            else:
                cancelled_id = cancel_last_accepted(stack, urgent_q, normal_q)
                print(f"Отменена последняя принятая заявка: {cancelled_id}")
        elif choice == "5":
            print_history(history)
        elif choice == "6":
            history.reverse()
            print("История развернута.")
        elif choice == "7":
            stats = get_statistics(history)
            for s in stats:
                print(f"{s['тип']}: всего={s['количество']}, срочных={s['срочных']}, "
                      f"среднее ожидание={s['среднее_ожидание']}, макс. ожидание={s['макс_ожидание']}")
        elif choice == "8":
            try:
                req_id = int(input("Введите номер заявки: ").strip())
                req = requests_by_id.get(req_id)
                if req:
                    print(f"Найдено: {req['клиент']} | {req['тип']} | {req['категория']} | {req['приоритет']}")
                else:
                    print("Заявка не найдена.")
            except ValueError:
                print("Ошибка: введите целое число.")
        elif choice == "9":
            stats = get_statistics(history)
            save_report("requests_report.txt", correct_count, errors, categories, stats, history)
            print("Отчёт сохранён в requests_report.txt")
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    q = Queue()
    q.enqueue(10)
    q.enqueue(20)
    assert q.dequeue() == 10
    assert q.dequeue() == 20
    try:
        q.dequeue()
        assert False
    except IndexError:
        pass

    q.enqueue({"номер": 1})
    q.enqueue({"номер": 2})
    assert q.remove_value(1) is True
    assert q.remove_value(3) is False

    s = Stack()
    s.push(5)
    s.push(7)
    assert s.pop() == 7
    assert s.pop() == 5
    try:
        s.pop()
        assert False
    except IndexError:
        pass

    ll = LinkedList()
    ll.add_in_tail({"номер": 1})
    ll.add_in_tail({"номер": 2})
    assert len(ll.to_list()) == 2
    assert ll.find(2)["номер"] == 2
    ll.reverse()
    assert ll.to_list()[0]["номер"] == 2

    main()