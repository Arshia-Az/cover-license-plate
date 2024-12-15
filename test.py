import cv2
import numpy as np
import easyocr

def blur_license_plate(image_path, custom_plate_path, output_path='output.jpg'):
    """
    شناسایی و جایگزینی پلاک ماشین در تصویر ورودی.
    
    :param image_path: مسیر تصویر ورودی
    :param custom_plate_path: مسیر تصویر دلخواه که باید به جای پلاک قرار گیرد
    :param output_path: مسیر ذخیره‌سازی تصویر خروجی
    """
    # خواندن تصویر ورودی
    image = cv2.imread(image_path)
    
    if image is None:
        print("تصویر یافت نشد. لطفاً مسیر تصویر را بررسی کنید.")
        return
    
    # تبدیل تصویر به مقیاس خاکستری برای بهبود دقت شناسایی
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # استفاده از EasyOCR برای شناسایی نواحی متن (پلاک)
    reader = easyocr.Reader(['fa', 'en'])
    results = reader.readtext(image_path)
    
    print(f"تعداد پلاک‌های شناسایی‌شده: {len(results)}")
    
    for (bbox, text, prob) in results:
        (x_min, y_min), (x_max, y_max) = bbox[0], bbox[2]
        width = x_max - x_min
        height = y_max - y_min
    
        # فیلتر بر اساس اندازه ناحیه (عرض و ارتفاع)
        if width > 100 and height > 30:  # مقادیر 100 و 30 را بر اساس نیاز تغییر دهید
            plate_region = image[int(y_min):int(y_max), int(x_min):int(x_max)]
            
            # خواندن تصویر سفارشی که باید به جای پلاک قرار بگیرد
            custom_plate = cv2.imread(custom_plate_path)
            
            if custom_plate is None:
                print("تصویر سفارشی یافت نشد. لطفاً مسیر تصویر را بررسی کنید.")
                return
            
            # تغییر اندازه تصویر دلخواه به اندازه ناحیه پلاک
            custom_plate_resized = cv2.resize(custom_plate, (int(width), int(height)))
            
            # جایگزینی ناحیه پلاک با تصویر دلخواه
            image[int(y_min):int(y_max), int(x_min):int(x_max)] = custom_plate_resized

    # ذخیره تصویر پردازش‌شده
    cv2.imwrite(output_path, image)
    
    print(f"تصویر خروجی ذخیره شد: {output_path}")
    
    # نمایش تصویر خروجی (اختیاری)
    cv2.imshow("Output", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # مسیر تصویر ورودی و تصویر دلخواه را تنظیم کنید
    input_image_path = 'C:\\Users\\User\\Desktop\\New folder\\car.jpg'  # مسیر تصویر خودرو که باید پردازش شود
    custom_plate_path = 'C:\\Users\\User\\Desktop\\New folder\\custom_plate.jpg'  # مسیر تصویر دلخواه برای جایگزینی پلاک
    output_image_path = 'C:\\Users\\User\\Desktop\\New folder\\output.jpg'  # مسیر ذخیره‌سازی تصویر خروجی
    
    # فراخوانی تابع برای جایگزینی پلاک خودرو با تصویر دلخواه
    blur_license_plate(input_image_path, custom_plate_path, output_image_path)
