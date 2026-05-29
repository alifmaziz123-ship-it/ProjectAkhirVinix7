DATA = {
    "meta": {
        "title": "D'Las Lembah Asri Serang Purbalingga",
        "source": "Google Maps Reviews",
        "total_data": 5296,
        "train_size": 4236,
        "test_size": 1060,
        "period": "2016 - 2024"
    },
    "distribution": {
        "sentiment": {"Positif": 4405, "Netral": 636, "Negatif": 255},
        "stars": {"1": 130, "2": 125, "3": 636, "4": 1690, "5": 2715}
    },
    "model_no_weight": {
        "accuracy": 0.8585,
        "macro_f1": 0.6496,
        "confusion_matrix": [[27, 4, 20], [10, 68, 49], [37, 30, 815]],
        "per_class": {
            "Negatif": {"precision": 0.3649, "recall": 0.5294, "f1": 0.432},
            "Netral": {"precision": 0.6667, "recall": 0.5354, "f1": 0.5939},
            "Positif": {"precision": 0.9219, "recall": 0.924, "f1": 0.923}
        }
    },
    "model_weighted": {
        "accuracy": 0.8151,
        "macro_f1": 0.6612,
        "confusion_matrix": [[42, 3, 6], [16, 96, 15], [61, 95, 726]],
        "per_class": {
            "Negatif": {"precision": 0.3529, "recall": 0.8235, "f1": 0.4941},
            "Netral": {"precision": 0.4948, "recall": 0.7559, "f1": 0.5981},
            "Positif": {"precision": 0.9719, "recall": 0.8231, "f1": 0.8913}
        },
        "weights": {"Negatif": 6.9216, "Netral": 2.7741, "Positif": 0.4008}
    },
    "yearly": {
        "years": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "avg_rating": [4.0, 3.74, 3.817, 3.875, 3.995, 4.249, 4.393, 4.421, 4.446],
        "count": [2, 100, 262, 384, 388, 1042, 1213, 928, 977],
        "sentiment_orig": {
            "Positif": [2, 64, 160, 278, 292, 860, 1054, 819, 876],
            "Netral": [0, 28, 84, 80, 78, 123, 108, 68, 67],
            "Negatif": [0, 8, 18, 26, 18, 59, 51, 41, 34]
        },
        "sentiment_weighted": {
            "Positif": [2, 56, 152, 234, 260, 724, 832, 698, 767],
            "Netral": [0, 32, 68, 88, 88, 166, 205, 133, 137],
            "Negatif": [0, 12, 42, 62, 40, 152, 176, 97, 73]
        }
    },
    "monthly_2024": {
        "months": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "month_names": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt"],
        "Positif": [112, 65, 35, 116, 115, 75, 120, 51, 116, 71],
        "Netral": [0, 8, 8, 8, 0, 14, 7, 0, 8, 14],
        "Negatif": [3, 0, 3, 14, 0, 0, 0, 0, 0, 14]
    },
    "neg_themes": {
        "Wahana Berbayar Lagi": 18,
        "Pelayanan Buruk": 16,
        "Harga Mahal": 10,
        "Stroberi Tidak Berbuah": 7,
        "Animal Abuse (Hewan)": 5,
        "Fasilitas Kurang": 4,
        "Kebersihan": 6
    },
    "top_words": {
        "Positif": [
            {"word": "tempat", "count": 1706}, {"word": "sejuk", "count": 1484},
            {"word": "banyak", "count": 1320}, {"word": "wahana", "count": 1166},
            {"word": "wisata", "count": 948}, {"word": "keluarga", "count": 907},
            {"word": "anak", "count": 846}, {"word": "tiket", "count": 845},
            {"word": "bagus", "count": 833}, {"word": "luas", "count": 696},
            {"word": "cocok", "count": 670}, {"word": "nyaman", "count": 517}
        ],
        "Negatif": [
            {"word": "masuk", "count": 54}, {"word": "bayar", "count": 44},
            {"word": "wisata", "count": 41}, {"word": "tiket", "count": 36},
            {"word": "foto", "count": 33}, {"word": "kurang", "count": 32},
            {"word": "burung", "count": 30}, {"word": "wahana", "count": 30},
            {"word": "cuma", "count": 24}, {"word": "tukang", "count": 24},
            {"word": "anak", "count": 23}, {"word": "binatang", "count": 15}
        ],
        "Netral": [
            {"word": "masuk", "count": 168}, {"word": "bayar", "count": 151},
            {"word": "bagus", "count": 138}, {"word": "tiket", "count": 119},
            {"word": "wahana", "count": 115}, {"word": "sejuk", "count": 108},
            {"word": "kurang", "count": 76}, {"word": "lumayan", "count": 63},
            {"word": "strawberry", "count": 58}, {"word": "harga", "count": 65},
            {"word": "area", "count": 58}, {"word": "kebun", "count": 63}
        ]
    },
    "samples": {
        "Positif": [
            {"stars": 5, "date": "2024-10-10", "text": "Seru buat piknik sama keluarga, harga terjangkau. Untuk masuk nya 10.000 ada tiket hemat terusan dari 35.000 untuk 1 org itu bisa masuk ke (dino land, mini zoo, taman kelinci) jauh lebih hemat. Ada playground juga."},
            {"stars": 5, "date": "2024-08-03", "text": "Parkirnya luas dan nyaman. Tiket masuknya murah hanya 10k dan parkir mobil 5k. Tempatnya luas dan sangat banyak pilihan wahana, seperti wahana air, kolam renang, kebun binatang, kebun strawberry. Tempat bersih dan nyaman."},
            {"stars": 5, "date": "2024-08-08", "text": "Cocok bgt buat destinasi liburan bareng temen atau juga keluarga. Ngadain gathering juga oke bgt karna ada aula yg lumayan luas. Tempatnya nyaman, fasilitasnya lengkap dan kebersihannya bener-bener terjaga."},
            {"stars": 4, "date": "2024-09-24", "text": "Tempatnya nyaman sejuk. Cocok buat santai atau bermain bersama keluarga. Banyak wahana bermain anak juga. Baru pertama ke sini belum ter-eksplorasi semua."},
            {"stars": 5, "date": "2024-08-12", "text": "Tempat rekreasi lengkap di daerah pegunungan. Banyak aktivitas yang bisa dilakukan, ada kebun binatang, taman kelinci, dino land, playground, kolam renang, petik strawberry."}
        ],
        "Negatif": [
            {"stars": 1, "date": "2024-04-14", "text": "Saya kasih bintang 1 karena saya menemukan yang termasuk 'animal abuse' di sini. Tempat ini ada kebun strawberry, hutan pinus sampai kebun binatang. Kebun binatang bagian satwa burung: burung dirantai kakinya sehingga tidak bisa terbang."},
            {"stars": 2, "date": "2024-10-17", "text": "Kangen D'Las yang dulu bayar tiket masuk cuma sekali, pas udah di dalem bebas mau jalan kemana saja. Sekarang masuk sana sini harus bayar lagi jadi males."},
            {"stars": 1, "date": "2022-09-13", "text": "Hujan lebat sejak masuk Desa Bojong Mrebet sampai di lokasi D'Las. Gerbang D'Las tutup, cuma sayangnya tanpa kopi sehingga dinginnya udara sekitar semakin menjadi-jadi."},
            {"stars": 2, "date": "2023-06-10", "text": "gede doang... toilet ngga ada... karyawannya pelit2... padahal baru keluar tadi... mau ikut toilet aja ga boleh... hadehh"},
            {"stars": 1, "date": "2023-08-20", "text": "Ada Robot Kuning, anak-anak mau foto malah menyingkir. Kalau memang harus bayar ya siap bayar, yang lainnya oke sih, hanya itu yang mengecewakan."}
        ],
        "Netral": [
            {"stars": 3, "date": "2024-10-04", "text": "Biaya masuk 10rb/org. Banyak area wisata didalamnya, ada HTM lagi per wisatanya. Kolam renang, kebun strawberry, kebun binatang mini, rumah kelinci. Niat ke D'Las mau petik strawberry, malah mahal banget."},
            {"stars": 3, "date": "2024-06-18", "text": "Tempatnya bagus, cuma pas siang terik banget padahal udaranya dingin seger. Kurangnya, pas metik strawberry masuknya bayar dan kalo metik hasilnya ditimbang terus bayar lagi."},
            {"stars": 3, "date": "2024-06-22", "text": "Klo bisa toiletnya jangan bayarlah walaupun 2rb, klo org yg beser bolak balik lumayan. Mending gabungin sekalian sama tiket masuk di depan. Udah itu aja, lainnya oke semua."},
            {"stars": 3, "date": "2023-07-17", "text": "Konsepnya keren memadukan wisata edukasi dan hiburan. Suasana khas wisata alam sangat terasa, dingin dan berkabut. Tapi prepare budget buat beberapa wahana yang ada."},
            {"stars": 3, "date": "2024-07-14", "text": "Kesan pertama sudah bagus untuk keseluruhan D'Las. Tapi ada yang perlu diperbaiki dari sisi manajemen antrian wahana yang kadang kurang teratur saat ramai."}
        ]
    }
}
