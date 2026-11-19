"""Perhitungan metode Weighted Product (WP)."""
import math


def weighted_product(alternatif, nilai, bobot, jenis):
    """
    alternatif : list nama alternatif
    nilai      : list baris nilai, satu baris per alternatif
    bobot      : list bobot awal per kriteria
    jenis      : list "benefit" / "cost" per kriteria
    Return: (w, pangkat, S, V, ranking)
    """
    total = sum(bobot)
    if total <= 0:
        raise ValueError("Total bobot harus lebih dari 0.")
    w = [b / total for b in bobot]
    pangkat = [wj if j == "benefit" else -wj for wj, j in zip(w, jenis)]

    S = []
    for nama, baris in zip(alternatif, nilai):
        # WP memakai pangkat, jadi nilai 0 atau negatif tidak bisa dihitung
        if any(x <= 0 for x in baris):
            raise ValueError(f"Nilai '{nama}' harus lebih dari 0 semua.")
        S.append(math.prod(x ** p for x, p in zip(baris, pangkat)))

    total_s = sum(S)
    V = [s / total_s for s in S]
    ranking = sorted(zip(alternatif, V), key=lambda t: t[1], reverse=True)
    return w, pangkat, S, V, ranking


if __name__ == "__main__":
    # Self-check dengan contoh perhitungan manual
    alt = ["A1", "A2", "A3", "A4"]
    data = [[6, 3, 2, 5, 25], [5, 4, 1, 4, 20], [7, 2, 3, 4, 20], [8, 3, 2, 5, 15]]
    w, p, S, V, rank = weighted_product(
        alt, data, [5, 4, 3, 4, 2], ["cost", "cost", "benefit", "benefit", "cost"]
    )
    assert [round(s, 4) for s in S] == [0.5346, 0.4584, 0.5849, 0.5223], S
    assert [n for n, _ in rank] == ["A3", "A1", "A4", "A2"], rank
    assert abs(sum(V) - 1) < 1e-9
    for i, (n, v) in enumerate(rank, 1):
        print(f"{i}. {n}  V = {v:.4f}")
    print("Self-check OK")
