import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. Matplotlibで図形を作成して保存
figure_path = "plot_image.png"
plt.figure()
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], label="Sample Plot")
plt.title("Example Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.savefig(figure_path, dpi=300, bbox_inches="tight")
plt.close()

# 2. ReportLabでPDFを生成
pdf_path = "output.pdf"
pdf = canvas.Canvas(pdf_path, pagesize=letter)

# 文章の追加
text = """This is an example of adding both text and a Matplotlib plot
into the same PDF file. You can customize the text and placement."""
pdf.drawString(100, 750, "Example PDF with Text and Plot")
pdf.drawString(100, 730, text)

# 画像の追加
pdf.drawImage(figure_path, 100, 400, width=400, height=300)  # x, y, 幅, 高さ

# PDF保存
pdf.save()

print(f"PDFを '{pdf_path}' に保存しました！")
