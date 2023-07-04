import os
import logging
import glob
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from fpdf import FPDF

logging.basicConfig(filename="response.log", level=logging.INFO)

createSticker_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(createSticker_dir, "tr-arial.ttf")
barcodes_dir = os.path.join(createSticker_dir, "barcodes")
png_files = glob.glob(os.path.join(barcodes_dir, "*.png"))

# altında "cargoTrackingNumber" verisi yazan ve yazmayan barkodların oluşturulması:
def generateBarcodes(cargoTrackingNumber):
    try:
        cargoTrackingNumber=str(cargoTrackingNumber)
        code128 = Code128(cargoTrackingNumber, writer=ImageWriter())
        
        options = {
        'module_width': 0.25,    
        'module_height': 6.5,    
        'font_size': 4.5,        
        'text_distance': 2,     
        'quiet_zone': 3,        
        }

        options2 = {
        'module_width': 0.25,    
        'module_height': 6.5,    
        'font_size': 0,          
        'text_distance': 0,      
        'quiet_zone': 3,
        }
        
        code128.save(f'barcodes/barcode{cargoTrackingNumber}', options=options)
        code128.save(f'barcodes/barcode{cargoTrackingNumber}numarasiz', options=options2)
    except Exception as e:
        err_msg = f"createStickers.py / generateBarcodes fonksiyonunda hata: {e}, {os.getcwd()}"
        logging.error(err_msg)

# sticker oluşturulması:
def createSticker(order):
    try:
        # order'dan alınacak parametreler:
        orderNumber = order.get("orderNumber", "")
        cargoTrackingNumber = order.get("cargoTrackingNumber", "")
        cargoProviderName = order.get("cargoProviderName", "")
        shipmentAddress = order.get("shipmentAddress", {})
        address1 = shipmentAddress.get("address1", "")
        neighborhood = shipmentAddress.get("neighborhood", "")
        district = shipmentAddress.get("district", "")
        city = shipmentAddress.get("city", "")
        fullName = shipmentAddress.get("fullName", "")

        firstBoxContent = address1 + "\n" + "\n"
        footerContent = orderNumber + "\n" + str(cargoTrackingNumber) + "\n" + cargoProviderName

        if neighborhood is not None:
            firstBoxContent += neighborhood + "\n" + "\n" + district + "/" + city
        else:
            firstBoxContent += "\n" + "\n" + district + "/" + city
        
        # 0) Kullanılacak barkodların oluşturulması:
        generateBarcodes(cargoTrackingNumber)

        img = Image.open(f'barcodes/barcode{cargoTrackingNumber}numarasiz.png')
        img = img.rotate(270, expand=True)
        img = img.save(f'barcodes/barcode{cargoTrackingNumber}numarasiz.png')

        # 1) PDF sayfası oluşturulması:

        # FPDF objesi
        # layout: ("P", "L")
        # unit: ("m", "cm", "in")
        # format ("A3", "A4" (default), "A5", "Letter", "Legal", (100w, 150h))
        pdf = FPDF("P", "mm", "A4")

        # sayfa oluştur
        pdf.add_page()

        # 2, 3) barkod ve numarasini yerlestir
        pdf.image(f'barcodes/barcode{cargoTrackingNumber}.png')
        pdf.set_xy(166, 48)
        pdf.image(f'barcodes/barcode{cargoTrackingNumber}numarasiz.png')

        # 4) Box1'i oluştur
        pdf.add_font("tr-arial","", font_path, uni=True)
        pdf.set_font("tr-arial", "", 16)
        pdf.set_auto_page_break(auto=True, margin=5)
        pdf.set_xy(18, 60)
        pdf.multi_cell(w=140, h=10, txt=firstBoxContent.upper(), border=1, align="L")

        # 5) Box2'yi oluştur
        cell_margin = 5
        pdf.set_y(pdf.get_y()+ cell_margin)
        pdf.set_x(18)
        pdf.cell(w=140, h=15, txt=fullName.upper(), border=1, align="L")
        
        # 6) "orderDetail" / "orderNumber"
        cell_margin2 = 20
        pdf.set_y(pdf.get_y()+ cell_margin2)
        pdf.set_x(18)
        pdf.multi_cell(w=140, h=10, txt=footerContent.upper(), align="L")

        # sticker pdf'inin oluşturulması
        pdf.output(f"stickers/sticker_{orderNumber}.pdf")

        # üretilmiş barkodların silinmesi
        png_files = glob.glob(os.path.join(barcodes_dir, "*.png"))

        for file_path in png_files:
            os.remove(file_path)  
    except Exception as e:
        err_msg = f"createStickers.py / createSticker fonksiyonunda hata: {e}, {os.getcwd()}"
        logging.error(err_msg)