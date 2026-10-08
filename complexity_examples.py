"""مثال‌های آموزشی هشت مرتبهٔ زمانی؛ اجرا و بررسی با کتابخانهٔ استاندارد."""

from itertools import combinations, combinations_with_replacement, product
from math import factorial
import random


def _tick(stats, name="steps"):
    """ثبت یک عملیات منتخب، در صورت درخواست شمارش."""
    if stats is not None:
        stats[name] = stats.get(name, 0) + 1


def first_item(values, stats=None):
    """دسترسی مستقیم به عضو اول؛ زمان ثابت برای فهرست غیرتهی."""
    if not values:
        raise ValueError("فهرست نباید خالی باشد.")
    _tick(stats)
    return values[0]


def binary_search(values, target, stats=None):
    """جست‌وجوی دودویی در فهرست صعودی؛ یک رخداد یا منفی یک."""
    low, high = 0, len(values) - 1
    while low <= high:
        _tick(stats)
        mid = low + (high - low) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def linear_max(values, stats=None):
    """یافتن بیشینه با یک پیمایش؛ هر عضو بعدی یک مقایسه دارد."""
    if not values:
        raise ValueError("فهرست نباید خالی باشد.")
    best = values[0]
    for index in range(1, len(values)):
        _tick(stats)
        if values[index] > best:
            best = values[index]
    return best


def merge_sort(values, stats=None):
    """مرتب‌سازی ادغامی؛ شمارنده تعداد نوشتن در بافر را ثبت می‌کند."""
    items = list(values)
    buffer = [None] * len(items)

    def merge(lo, mid, hi):
        left, right, out = lo, mid, lo
        while left < mid and right < hi:
            if items[left] <= items[right]:
                buffer[out] = items[left]
                left += 1
            else:
                buffer[out] = items[right]
                right += 1
            _tick(stats)
            out += 1
        while left < mid:
            buffer[out] = items[left]
            _tick(stats)
            left += 1
            out += 1
        while right < hi:
            buffer[out] = items[right]
            _tick(stats)
            right += 1
            out += 1
        for index in range(lo, hi):
            items[index] = buffer[index]

    def sort_range(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort_range(lo, mid)
        sort_range(mid, hi)
        merge(lo, mid, hi)

    sort_range(0, len(items))
    return items


def selection_sort(values, stats=None):
    """مرتب‌سازی انتخابی؛ خروجی جدید می‌سازد و ورودی را تغییر نمی‌دهد."""
    items = list(values)
    for first in range(len(items) - 1):
        minimum = first
        for index in range(first + 1, len(items)):
            _tick(stats)
            if items[index] < items[minimum]:
                minimum = index
        if minimum != first:
            items[first], items[minimum] = items[minimum], items[first]
    return items


def matrix_multiply(left, right, stats=None):
    """ضرب معمولی دو ماتریس مربعی؛ شمارنده تعداد ضرب‌های عددی است."""
    n = len(left)
    if len(right) != n or any(len(row) != n for row in left + right):
        raise ValueError("دو ماتریس باید مربعی و هم‌اندازه باشند.")
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                _tick(stats)
                result[i][j] += left[i][k] * right[k][j]
    return result


def count_subset_sums(values, target, stats=None):
    """شمارش زیرمجموعه‌های دارای مجموع هدف با انتخاب یا حذف هر عضو."""
    n = len(values)

    def visit(index, total):
        _tick(stats, "nodes")
        if index == n:
            _tick(stats, "leaves")
            return int(total == target)
        without_current = visit(index + 1, total)
        with_current = visit(index + 1, total + values[index])
        return without_current + with_current

    return visit(0, 0)


def count_permutations(values, stats=None):
    """شمارش ترتیب‌های موقعیت‌ها با پیمایش همهٔ جایگشت‌ها؛ بدون کپی در برگ."""
    items = list(values)
    n = len(items)

    def visit(first):
        _tick(stats, "nodes")
        if first == n:
            _tick(stats, "leaves")
            return 1
        total = 0
        for index in range(first, n):
            items[first], items[index] = items[index], items[first]
            total += visit(first + 1)
            # بازگرداندن وضعیت برای بررسی انتخاب بعدی.
            items[first], items[index] = items[index], items[first]
        return total

    return visit(0)


def run_checks():
    """بررسی پاسخ‌ها با مرجع مستقل و کنترل شمار عملیات منتخب."""
    totals = {"دسترسی و بیشینه": 0, "جست‌وجو": 0, "مرتب‌سازی": 0,
              "ضرب ماتریس": 0, "زیرمجموعه": 0, "جایگشت": 0, "شمار عملیات": 0}
    for function in (first_item, linear_max):
        try:
            function([])
        except ValueError:
            totals["دسترسی و بیشینه"] += 1
        else:
            raise AssertionError("ورودی خالی باید خطای مشخص داشته باشد.")

    for n in range(7):
        for values in product(range(3), repeat=n):
            values = list(values)
            before = values.copy()
            for function in (selection_sort, merge_sort):
                assert function(values) == sorted(values)
                assert values == before
                totals["مرتب‌سازی"] += 1
            if values:
                assert first_item(values) == values[0]
                assert linear_max(values) == max(values)
                totals["دسترسی و بیشینه"] += 2

    for n in range(7):
        for values in combinations_with_replacement(range(5), n):
            values = list(values)
            for target in range(-1, 6):
                answer = binary_search(values, target)
                if target in values:
                    assert 0 <= answer < len(values) and values[answer] == target
                else:
                    assert answer == -1
                totals["جست‌وجو"] += 1

    assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    totals["ضرب ماتریس"] += 1
    rng = random.Random(20261008)
    for n in range(6):
        for _ in range(10):
            matrix = [[rng.randrange(-5, 6) for _ in range(n)] for _ in range(n)]
            identity = [[int(i == j) for j in range(n)] for i in range(n)]
            zero = [[0] * n for _ in range(n)]
            assert matrix_multiply(matrix, identity) == matrix
            assert matrix_multiply(identity, matrix) == matrix
            assert matrix_multiply(matrix, zero) == zero
            totals["ضرب ماتریس"] += 3
    for left, right in [([[1, 2]], [[1]]), ([[1]], [[1, 2]]), ([], [[1]])]:
        try:
            matrix_multiply(left, right)
        except ValueError:
            totals["ضرب ماتریس"] += 1
        else:
            raise AssertionError("ابعاد نامعتبر باید تشخیص داده شوند.")

    for n in range(6):
        for values in product(range(3), repeat=n):
            for target in range(-1, 9):
                expected = sum(sum(chosen) == target for size in range(n + 1)
                               for chosen in combinations(values, size))
                assert count_subset_sums(values, target) == expected
                totals["زیرمجموعه"] += 1

    for n in range(9):
        data = list(range(n))
        before = data.copy()
        stats = {}
        assert count_permutations(data, stats) == factorial(n)
        assert stats["leaves"] == factorial(n)
        assert stats["nodes"] == sum(factorial(n) // factorial(n - k) for k in range(n + 1))
        assert data == before
        totals["جایگشت"] += 1

    for n in (1, 2, 4, 8, 16):
        data = list(range(n))
        stats = {}
        first_item(data, stats)
        assert stats["steps"] == 1
        stats = {}
        binary_search(data, n, stats)
        assert stats["steps"] == n.bit_length()
        stats = {}
        linear_max(data, stats)
        assert stats.get("steps", 0) == n - 1
        stats = {}
        merge_sort(data, stats)
        assert stats.get("steps", 0) == n * (n.bit_length() - 1)
        stats = {}
        selection_sort(data, stats)
        assert stats.get("steps", 0) == n * (n - 1) // 2
        totals["شمار عملیات"] += 5
    for n in range(7):
        stats = {}
        matrix_multiply([[1] * n for _ in range(n)], [[1] * n for _ in range(n)], stats)
        assert stats.get("steps", 0) == n**3
        stats = {}
        count_subset_sums(list(range(n)), 3, stats)
        assert stats["leaves"] == 2**n and stats["nodes"] == 2 ** (n + 1) - 1
        totals["شمار عملیات"] += 2
    return totals


if __name__ == "__main__":
    for label, total in run_checks().items():
        print(f"بررسی {label}: {total} حالت موفق")
    print("نتیجه: همهٔ بررسی‌ها موفق بودند.")
