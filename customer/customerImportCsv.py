import csv
import io
from django.shortcuts import render


def upload_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # ファイルオブジェクトをテキストモードに変換（UTF-8）
        # Excelで作成したCSVの場合は 'shift_jis' や 'cp932' を指定
        data_set = csv_file.read().decode("utf-8")
        io_string = io.StringIO(data_set)

        # CSVを1行ずつループ処理
        reader = csv.reader(io_string, delimiter=",")

        # 1行目がヘッダー（列名）の場合は next() でスキップ可能
        # header = next(reader)

        for row in reader:
            # rowは配列です。例：['田中', '30', '東京都']
            print(row)

            # ここでデータベースに保存する処理（モデルの作成など）を行う
            # MyModel.objects.create(name=row[0], age=row[1], city=row[2])

        return render(request, "success.html")

    return render(request, "upload.html")

