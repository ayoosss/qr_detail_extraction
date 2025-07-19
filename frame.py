import qrcode
from PIL import Image
import re
import sys

def validate_date(date_text):
    # Validate date format YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_text):
        return False
    return True

def generate_employee_qr(name, employee_id, dob):
    # Prepare the data string to encode in the QR code
    data = f"Name: {name}\nEmployee ID: {employee_id}\nDOB: {dob}"
    
    # Save the input data to employee_data.dat
    try:
        with open("employee_data.dat", "a") as f:
            f.write(f"{name},{employee_id},{dob}\n")
    except Exception as e:
        print(f"Error saving employee data: {e}")
        sys.exit(1)
    
    # Create qr code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the instance
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image file
    filename = f"employee_{employee_id}_qr.png"
    try:
        img.save(filename)
        print(f"QR code saved as {filename}")
    except Exception as e:
        print(f"Error saving QR code image: {e}")
        sys.exit(1)
    
    # Optionally show the image
    img.show()

def main():
    print("Enter employee details to generate QR code:")
    
    while True:
        name = input("Name (max 50 chars): ").strip()
        if 0 < len(name) <= 50:
            break
        print("Invalid input. Please enter a non-empty name up to 50 characters.")
    
    while True:
        employee_id = input("Employee ID (max 20 chars): ").strip()
        if 0 < len(employee_id) <= 20:
            break
        print("Invalid input. Please enter a non-empty employee ID up to 20 characters.")
    
    while True:
        dob = input("Date of Birth (YYYY-MM-DD): ").strip()
        if validate_date(dob):
            break
        print("Invalid date format. Please enter date in YYYY-MM-DD format.")
    
    generate_employee_qr(name, employee_id, dob)

if __name__ == "__main__":
    main()
