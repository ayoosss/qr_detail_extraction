import cv2
from pyzbar import pyzbar
import sys

def validate_qr_data(data):
    # Basic validation: check if data contains required fields in expected format
    # Expected format: Name: <name>\\nEmployee ID: <id>\\nDOB: <dob>
    lines = data.split('\\n')
    if len(lines) != 3:
        return False
    if not lines[0].startswith("Name: "):
        return False
    if not lines[1].startswith("Employee ID: "):
        return False
    if not lines[2].startswith("DOB: "):
        return False
    return True

def save_registered_data(data):
    # Save the scanned data to registered_data.dat
    try:
        with open("registered_data.dat", "a") as f:
            # Save as CSV format: name,employee_id,dob
            lines = data.split('\\n')
            name = lines[0][len("Name: "):].strip()
            employee_id = lines[1][len("Employee ID: "):].strip()
            dob = lines[2][len("DOB: "):].strip()
            f.write(f"{name},{employee_id},{dob}\\n")
    except Exception as e:
        print(f"Error saving registered data: {e}")
        sys.exit(1)

import sys

def main():
    print("Starting QR code scanner. Press 'q' to quit.")
    # Use camera index from command line argument if provided, else default to 0
    camera_index = 0
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            print("Invalid camera index argument. Using default camera 0.")
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Cannot open camera with index {camera_index}")
        sys.exit(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            if validate_qr_data(qr_data):
                print("Valid QR code detected:")
                print(qr_data)
                save_registered_data(qr_data)
                print("Data registered successfully.")
            else:
                print("Invalid QR code detected. Exception raised.")
                cap.release()
                cv2.destroyAllWindows()
                raise Exception("Scanned QR code is not generated from frame.py")

            # Draw rectangle around QR code
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
