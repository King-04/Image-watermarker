import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk


class ImageWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")

        # Variables
        self.image_path = tk.StringVar()
        self.watermark_text = tk.StringVar()

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Image Selection
        tk.Label(self.root, text="Select Image:").pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_image).pack(pady=5)

        # Watermark Text Entry
        tk.Label(self.root, text="Watermark Text:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.watermark_text).pack(pady=5)

        # Watermark Button
        tk.Button(self.root, text="Watermark Image", command=self.watermark_image).pack(pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path.set(file_path)
            self.display_image(file_path)

    def display_image(self, path):
        image = Image.open(path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.root, image=photo)
        label.image = photo
        label.pack(pady=10)

    def watermark_image(self):
        image_path = self.image_path.get()
        watermark_text = self.watermark_text.get()

        if not image_path or not watermark_text:
            messagebox.showerror("Error", "Please select an image and enter a watermark text.")
            return

        original_image = Image.open(image_path)
        watermark = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(watermark)
        font = ImageFont.load_default()  # Try to load the default font

        if font is None:
            # If the default font is not available, use a built-in font
            font = ImageFont.load_default()

        text_width, text_height = draw.textbbox((0, 0), watermark_text, font=font)[:2]
        text_width += 10  # Add some padding for better positioning
        text_height += 10  # Add some padding for better positioning

        # Calculate the center position
        x = (original_image.width - text_width) // 2
        y = (original_image.height - text_height) // 2

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

        watermarked_image = Image.alpha_composite(original_image.convert("RGBA"), watermark)

        # Save the watermarked image
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            watermarked_image.save(save_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageWatermarkApp(root)
    root.mainloop()
