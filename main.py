import cv2
import os


def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))


def encode_message(image_path, message, output_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read the image at {image_path}")

    # Convert message to binary
    binary_message = text_to_binary(message) + '1111111111111110'  # Add delimiter

    # Check if the image is big enough to store the message
    if len(binary_message) > img.shape[0] * img.shape[1] * 3:
        raise ValueError("Image is too small to store the message")

    # Flatten the image
    img_flat = img.flatten()

    # Modify the least significant bits
    for i, bit in enumerate(binary_message):
        img_flat[i] = (img_flat[i] & 0xFE) | int(bit)

    # Reshape the image back to its original shape
    stego_img = img_flat.reshape(img.shape)

    # Determine the file extension and save the image
    _, ext = os.path.splitext(output_path)
    if ext.lower() not in ['.png', '.bmp', '.tiff', '.tif']:
        print(f"Warning: {ext} format may not preserve the hidden message. Converting to PNG.")
        output_path = os.path.splitext(output_path)[0] + '.png'

    success = cv2.imwrite(output_path, stego_img)
    if not success:
        raise IOError(f"Failed to save the image at {output_path}")
    print(f"Message encoded successfully. Output saved to {output_path}")


def decode_message(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read the image at {image_path}")

    # Flatten the image
    img_flat = img.flatten()

    # Extract the least significant bits
    binary_message = ''.join([str(pixel & 1) for pixel in img_flat])

    # Find the delimiter
    delimiter_index = binary_message.find('1111111111111110')
    if delimiter_index == -1:
        raise ValueError("No hidden message found")

    # Extract the message
    extracted_binary = binary_message[:delimiter_index]
    extracted_message = binary_to_text(extracted_binary)

    return extracted_message


def main():
    while True:
        print("\nSteganography Tool")
        print("1. Encode a message")
        print("2. Decode a message")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            image_path = input("Enter the path to the input image: ")
            message = input("Enter the message to hide: ")
            output_path = input("Enter the path for the output image: ")
            try:
                encode_message(image_path, message, output_path)
            except Exception as e:
                print(f"Error: {str(e)}")
        elif choice == '2':
            image_path = input("Enter the path to the image with hidden message: ")
            try:
                decoded_message = decode_message(image_path)
                print(f"Decoded message: {decoded_message}")
            except Exception as e:
                print(f"Error: {str(e)}")
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
