import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from matplotlib import pyplot as plt
from datetime import datetime
import os
from PIL import Image, ImageTk, ImageGrab

def mse(imageA, imageB):
    """Calculate the Mean Squared Error between two images."""
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def psnr(imageA, imageB):
    """Calculate the Peak Signal-to-Noise Ratio between two images."""
    mse_value = mse(imageA, imageB)
    if mse_value == 0:
        return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(mse_value))

def normalized_cross_correlation(imageA, imageB):
    """Calculate Normalized Cross-Correlation between two images."""
    return np.sum((imageA - np.mean(imageA)) * (imageB - np.mean(imageB))) / (np.std(imageA) * np.std(imageB) * imageA.size)

def entropy(image):
    """Calculate the entropy of an image."""
    hist, _ = np.histogram(image.ravel(), bins=256, range=(0, 256))
    hist = hist / hist.sum()
    entropy_value = -np.sum(hist * np.log2(hist + 1e-10))  # Add epsilon to avoid log(0)
    return entropy_value

def compare_images(imageA, imageB):
    """Compare two images and compute MSE, PSNR, SSIM, NCC, and entropy difference."""
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    m = mse(grayA, grayB)
    p = psnr(grayA, grayB)
    s = ssim(grayA, grayB)
    ncc = normalized_cross_correlation(grayA, grayB)
    entropy_diff = abs(entropy(grayA) - entropy(grayB))
    return m, p, s, ncc, entropy_diff

def file_size(filepath):
    """Get file size in bytes."""
    return os.path.getsize(filepath)

def analyze_metric(metric_value, ranges):
    """Analyze metric based on predefined ranges and return qualitative label."""
    for label, (min_val, max_val) in ranges.items():
        if min_val <= metric_value <= max_val:
            return label
    return "Out of Range"

def plot_color_histograms(original, modified):
    """Plot color histograms for the original and modified images side by side."""
    colors = ('b', 'g', 'r')  # Blue, Green, Red
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Create subplots for histograms
    plt.suptitle('Color Histograms', fontsize=16)

    for i, color in enumerate(colors):
        hist_orig = cv2.calcHist([original], [i], None, [256], [0, 256])
        axs[0].plot(hist_orig, color=color, label=f'Original {color.upper()}')
        axs[0].set_xlim([0, 256])
        axs[0].set_title('Original Image Histogram')
        axs[0].set_xlabel('Pixel Value')
        axs[0].set_ylabel('Frequency')

        hist_mod = cv2.calcHist([modified], [i], None, [256], [0, 256])
        axs[1].plot(hist_mod, color=color, linestyle='dashed', label=f'Modified {color.upper()}')
        axs[1].set_xlim([0, 256])
        axs[1].set_title('Modified Image Histogram')
        axs[1].set_xlabel('Pixel Value')
        axs[1].set_ylabel('Frequency')

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout
    return fig  # Return the figure object

def display_graphs(mse_value, psnr_value, ssim_value, ncc_value, entropy_diff, original_size, modified_size):
    """Display bar graphs for various image comparison metrics."""
    metrics = ['MSE', 'PSNR', 'SSIM', 'NCC', 'Entropy Diff']
    values = [mse_value, psnr_value, ssim_value, ncc_value, entropy_diff]

    # Define ranges for qualitative analysis of metrics
    ranges = {
        'MSE': {'Perfect': (0, 0.1), 'Good Quality': (0.1, 1), 'Poor Quality': (1, float('inf'))},
        'PSNR': {'Excellent Quality': (40, float('inf')), 'Good Quality': (30, 40), 'Poor Quality': (0, 30)},
        'SSIM': {'Perfect Similarity': (1, 1), 'Excellent Similarity': (0.9, 1), 'Moderate Similarity': (0.7, 0.9), 'Low Similarity': (0, 0.7)},
        'NCC': {'Perfect Similarity': (1, 1), 'Excellent Similarity': (0.9, 1), 'Moderate Similarity': (0.7, 0.9), 'Low Similarity': (0, 0.7)},
        'Entropy Diff': {'Very Similar': (0, 0.5), 'Similar': (0.5, 1), 'Dissimilar': (1, float('inf'))}
    }

    # Set figure size to 19.2 x 10.8 inches for fullscreen appearance
    fig, ax = plt.subplots(figsize=(19.2, 10.8))  # Fullscreen aspect ratio 16:9

    # Plot primary metrics with qualitative labels
    bars = ax.bar(metrics, values, color=['blue', 'orange', 'green', 'red', 'purple'])
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values')
    ax.set_title('Image Comparison Metrics')

    # Add labels above bars based on analysis
    for i, bar in enumerate(bars):
        label = analyze_metric(values[i], ranges[metrics[i]])
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, label, ha='center', va='bottom')

    # Display ranges in a table format below the graph
    table_data = [
        ["Metric", "Perfect", "Good/Excellent Quality", "Moderate", "Poor/Low Quality"],
        ["MSE", "0", "<1", "N/A", ">1"],
        ["PSNR", "N/A", ">40 dB", "30-40 dB", "<30 dB"],
        ["SSIM", "1", ">0.9", "0.7-0.9", "<0.7"],
        ["NCC", "1", ">0.9", "0.7-0.9", "<0.7"],
        ["Entropy Diff", "0-0.5", "<1", "N/A", ">1"]
    ]

    # Use plt.table to add the index table
    the_table = plt.table(cellText=table_data, colLabels=None, cellLoc='center', loc='bottom', bbox=[0.1, -0.3, 0.8, 0.2])
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)

    # Adjust plot layout for table display
    plt.subplots_adjust(left=0.2, right=0.8, bottom=0.25)
    return fig  # Return the current figure



def save_results(original_path, modified_path, histogram_fig, metrics_fig):
    """Save images and metrics."""
    # Create subfolder based on original and modified image names
    original_name = os.path.splitext(os.path.basename(original_path))[0]
    modified_name = os.path.splitext(os.path.basename(modified_path))[0]
    
    subfolder_name = f"{original_name}_vs_{modified_name}"
    
    # Create the full path for saving results
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "result and analysis pictures", subfolder_name)
    os.makedirs(results_dir, exist_ok=True)

    # Save histograms and metrics as images
    histogram_fig.savefig(os.path.join(results_dir, f"histogram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
    metrics_fig.savefig(os.path.join(results_dir, f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))

    # Save the current screen (home page) as an image
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    x1 = x + root.winfo_width()
    y1 = y + root.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(os.path.join(results_dir, f"homepage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))

def load_and_compare_images(original_path, modified_path):
    """Load images, compare them, and generate the required figures."""
    # Load original and modified images
    original_image = cv2.imread(original_path)
    modified_image = cv2.imread(modified_path)

    # Convert images to RGB format
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    modified_image = cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB)

    # Calculate metrics
    mse_value, psnr_value, ssim_value, ncc_value, entropy_diff = compare_images(original_image, modified_image)

    original_size = file_size(original_path)
    modified_size = file_size(modified_path)
    size_diff = abs(original_size - modified_size)

    histogram_fig = plot_color_histograms(original_image, modified_image)
    metrics_fig = display_graphs(mse_value, psnr_value, ssim_value, ncc_value, entropy_diff, original_size, modified_size)

    return histogram_fig, metrics_fig, original_image, modified_image, mse_value, psnr_value, ssim_value, ncc_value, entropy_diff, size_diff, original_size, modified_size

def select_images():
    """Open file dialog to select original and modified images."""
    global original_path, modified_path  # Declare these as global variables to access them later
    original_path = filedialog.askopenfilename(title="Select Original Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not original_path:
        return  # Exit if no image is selected

    modified_path = filedialog.askopenfilename(title="Select Modified Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not modified_path:
        return  # Exit if no image is selected

    # Load and compare images
    histogram_fig, metrics_fig, original_image, modified_image, mse_value, psnr_value, ssim_value, ncc_value, entropy_diff, size_diff, original_size, modified_size = load_and_compare_images(original_path, modified_path)

    # Display images and metrics on main screen
    display_images_and_metrics(original_image, modified_image, mse_value, psnr_value, ssim_value, ncc_value, entropy_diff, histogram_fig, metrics_fig)

def display_images_and_metrics(original_image, modified_image, mse_value, psnr_value, ssim_value, ncc_value, entropy_diff, histogram_fig, metrics_fig):
    """Display the original and modified images along with metrics on the main window."""
    
    # Display Original Image
    orig_img = Image.fromarray(original_image)  # Convert to PIL Image
    orig_img = orig_img.resize((300, 300), Image.LANCZOS)  # Resize for display
    orig_img = ImageTk.PhotoImage(orig_img)

    original_label.config(image=orig_img)
    original_label.image = orig_img  # Keep a reference to avoid garbage collection

    # Display Modified Image
    mod_img = Image.fromarray(modified_image)  # Convert to PIL Image
    mod_img = mod_img.resize((300, 300), Image.LANCZOS)  # Resize for display
    mod_img = ImageTk.PhotoImage(mod_img)

    modified_label.config(image=mod_img)
    modified_label.image = mod_img  # Keep a reference to avoid garbage collection

    # Display Image Names
    orig_name_display = os.path.basename(original_path)  # Get original image filename
    mod_name_display = os.path.basename(modified_path)  # Get modified image filename
    
    # Create or update name labels
    original_name_label.config(text=f"Original: {orig_name_display}")
    modified_name_label.config(text=f"Modified: {mod_name_display}")

    # Get file sizes
    original_size_bytes = file_size(original_path)
    modified_size_bytes = file_size(modified_path)

    # Convert sizes to MB
    original_size_mb = original_size_bytes / (1024 * 1024)  # Convert to MB
    modified_size_mb = modified_size_bytes / (1024 * 1024)  # Convert to MB

    # Calculate size difference
    size_difference = modified_size_bytes - original_size_bytes
    size_change = "increased" if size_difference > 0 else "decreased" if size_difference < 0 else "same"

    # Prepare metrics text with modified size in MB and difference
    metrics_text = (f"MSE: {mse_value:.4f}\n"
                    f"PSNR: {psnr_value:.4f} dB\n"
                    f"SSIM: {ssim_value:.4f}\n"
                    f"NCC: {ncc_value:.4f}\n"
                    f"Entropy Diff: {entropy_diff:.4f}\n"
                    f"Original Size: {original_size_mb:.2f} MB\n"
                    f"Modified Size: {modified_size_mb:.2f} MB ({size_change} by {abs(size_difference / (1024 * 1024)):.2f} MB)\n")
    
    metrics_label.config(text=metrics_text)


def show_histogram():
    """Show the histogram figure in a new window."""
    if original_path and modified_path:
        histogram_fig, _ = load_and_compare_images(original_path, modified_path)[:2]
        histogram_fig.show()  # Open histogram in a new window
    else:
        messagebox.showwarning("Warning", "No images selected to display histogram.")

def show_graph():
    """Show the metrics figure in a new window."""    
    if original_path and modified_path:
        _, metrics_fig = load_and_compare_images(original_path, modified_path)[:2]
        metrics_fig.set_size_inches(19.2, 10.8)  # Ensure figure size matches fullscreen
        metrics_fig.savefig("metrics.png", dpi=300)  # Save the figure with higher dpi for better quality
        metrics_fig.show()  # Open metrics in a new window
    else:
        messagebox.showwarning("Warning", "No images selected to display graph.")


def save_pixel_comparison(original_image, modified_image, original_path, modified_path):
    """Save RGB pixel values comparison of the original and modified images to a text file."""
    # Create subfolder for results if it doesn't exist
    original_name = os.path.splitext(os.path.basename(original_path))[0]
    modified_name = os.path.splitext(os.path.basename(modified_path))[0]
    
    subfolder_name = f"{original_name}_vs_{modified_name}"
    
    # Create the full path for saving results
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "result and analysis pictures", subfolder_name)
    os.makedirs(results_dir, exist_ok=True)

    # Define the path for the text file
    text_file_path = os.path.join(results_dir, f"pixel_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    # Get the dimensions of the images
    height, width, _ = original_image.shape
    
    with open(text_file_path, 'w') as f:
        f.write("Original (R,G,B)\tModified (R,G,B)\n")  # Header for the file
        for y in range(height):
            for x in range(width):
                # Get pixel values for original and modified images
                orig_pixel = tuple(original_image[y, x])
                mod_pixel = tuple(modified_image[y, x])
                
                # Determine if the pixel value has changed
                if orig_pixel != mod_pixel:
                    f.write(f"({orig_pixel[0]},{orig_pixel[1]},{orig_pixel[2]} Changed)\t"
                            f"({mod_pixel[0]},{mod_pixel[1]},{mod_pixel[2]})\n")
                else:
                    # Write unchanged pixel values as is
                    f.write(f"({orig_pixel[0]},{orig_pixel[1]},{orig_pixel[2]})\t"
                            f"({mod_pixel[0]},{mod_pixel[1]},{mod_pixel[2]})\n")

    messagebox.showinfo("Success", f"Pixel comparison saved successfully to:\n{text_file_path}")


def save_results_button():
    """Save results when the save button is clicked."""
    if original_path and modified_path:
        # Save all results, including the figures and the screen capture
        histogram_fig, metrics_fig = load_and_compare_images(original_path, modified_path)[:2]
        save_results(original_path, modified_path, histogram_fig, metrics_fig)  # Save figures and screen capture
        # Add call to save pixel comparison
        original_image = cv2.imread(original_path)
        modified_image = cv2.imread(modified_path)
        save_pixel_comparison(original_image, modified_image, original_path, modified_path)  # Call new function
        messagebox.showinfo("Success", "Results saved successfully!")
    else:
        messagebox.showwarning("Warning", "No images selected to save results.")


def main():
    """Main function to set up the GUI."""
    global root, original_label, modified_label, metrics_label, histogram_frame, metrics_frame
    global original_path, modified_path, original_name_label, modified_name_label

    original_path = None
    modified_path = None

    root = tk.Tk()
    root.title("Image Comparison Tool")

    # Create Frames for displaying images and metrics
    original_label = Label(root)
    original_label.pack(side='left', padx=10)

    modified_label = Label(root)
    modified_label.pack(side='right', padx=10)

    # Labels for image names
    original_name_label = Label(root, text="", padx=20, pady=10)
    original_name_label.pack(side='left', padx=10)

    modified_name_label = Label(root, text="", padx=20, pady=10)
    modified_name_label.pack(side='right', padx=10)

    metrics_label = Label(root, text="", padx=20, pady=20)
    metrics_label.pack()

    histogram_frame = tk.Frame(root)
    histogram_frame.pack(side='bottom', padx=10, pady=10)

    metrics_frame = tk.Frame(root)
    metrics_frame.pack(side='bottom', padx=10, pady=10)

    Label(root, text="Choose original and modified images for comparison:", padx=20, pady=20).pack()
    Button(root, text="Select Images", command=select_images, padx=10, pady=5).pack()
    Button(root, text="Save Results", command=save_results_button, padx=10, pady=5).pack()
    Button(root, text="Show Histogram", command=show_histogram, padx=10, pady=5).pack()  # New button for histogram
    Button(root, text="Show Graph", command=show_graph, padx=10, pady=5).pack()  # New button for graph

    root.mainloop()

if __name__ == "__main__":
    main()
