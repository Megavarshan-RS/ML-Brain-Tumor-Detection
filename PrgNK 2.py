import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from docx import Document
#from docx.shared import Inches

class WhiteSectionAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tumor Analyzer")
        
        # Set background color to black
        self.root.configure(bg="black")

        self.image_paths = []

        self.age_label = tk.Label(root, text="Input MRI >", font=('aquire',12,'bold'),fg="blue", bg="black")
        self.age_label.pack(side=tk.LEFT)
        self.frame_original = tk.Frame(root, bg="black")
        self.frame_original.pack(side=tk.LEFT, padx=3, pady=3)

        self.age_label = tk.Label(root, text="Tumor Region >", font=('aquire', 12,'bold'), fg="green",bg="black")
        self.age_label.pack(side=tk.LEFT)
        self.frame_marked = tk.Frame(root, bg="black")
        self.frame_marked.pack(side=tk.LEFT, padx=10, pady=3)

        
        self.canvas_original = tk.Canvas(self.frame_original, width=250, height=250, bg="black")
        self.canvas_original.pack()

        self.canvas_marked = tk.Canvas(self.frame_marked, width=250, height=250, bg="black")
        self.canvas_marked.pack()

        self.result_label = tk.Label(root, text="", font=('Helvetica', 14), fg="red", bg="black")
        self.result_label.pack(pady=10)

        self.figure, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas_graph = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_graph_widget = self.canvas_graph.get_tk_widget()
        self.canvas_graph_widget.pack()

        self.age_label = tk.Label(root, text=" ",bg="black")
        self.age_label.pack()
        self.name_label = tk.Label(root, text="Patient Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()
        self.age_label = tk.Label(root, text=" ",bg="black")
        self.age_label.pack()
        self.age_label = tk.Label(root, text="Patient Age:")
        self.age_label.pack()

        self.age_entry = tk.Entry(root)
        self.age_entry.pack()
        self.age_label = tk.Label(root, text=" ",bg="black")
        self.age_label.pack()
        self.contact_label = tk.Label(root, text="Contact Number:")
        self.contact_label.pack()

        self.contact_entry = tk.Entry(root)
        self.contact_entry.pack()
        self.age_label = tk.Label(root, text=" ",bg="black")
        self.age_label.pack()
        self.address_label = tk.Label(root, text="Address:")
        self.address_label.pack()

        
        self.address_entry = tk.Entry(root)
        
        self.address_entry.pack()

        self.age_label = tk.Label(root, text=" ",bg="black")
        self.age_label.pack()
        self.analyze_button = tk.Button(root, text="Click Here To Browse Image", command=self.analyze_images, width=20, height=1, bg="blue", fg="white")
        self.analyze_button.pack()

        self.age_label = tk.Label(root, text=" ",bg="black")
        self.age_label.pack()
        self.quit_button = tk.Button(root, text="Quit", command=root.destroy, width=20, height=1, bg="red", fg="black")
        self.quit_button.pack()



    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return ImageTk.PhotoImage(Image.fromarray(image))

    def display_image(self, canvas, image_path):
        image = self.load_image(image_path)
        canvas.config(width=image.width(), height=image.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=image, tags="bg")
        canvas.image = image  # Save reference to avoid garbage collection

    def analyze_images(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get()

        # Store details in a string variable
        
        self.image_paths = filedialog.askopenfilenames(title="Select Image(s)", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        percentage_covered_list = []

        for i, image_path in enumerate(self.image_paths):
            marked_image, percentage_covered = self.k_meansClustering(image_path)

            # Display original image
            self.display_image(self.canvas_original, image_path)

            # Display marked image
            marked_image_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(marked_image, cv2.COLOR_BGR2RGB)))
            self.canvas_marked.config(width=marked_image_tk.width(), height=marked_image_tk.height())
            self.canvas_marked.create_image(0, 0, anchor=tk.NW, image=marked_image_tk)
            self.canvas_marked.image = marked_image_tk  # Save reference to avoid garbage collection

            # Print percentage covered
            result_text = f"{percentage_covered:.2f}% of Tumor Presence\n"
            self.result_label.config(text=result_text)
            details_string = f"\n\nName: {name} \nAge: {age} \nContact: {contact} \nAddress: {address} \n\nResult: {result_text}"
            

        # Replace 'path/to/your/image.jpg' with the path to your image
            input_image_path = image_path

# Replace 'output_document.docx' with the desired output Word document name
            output_word_document = name+'_'+contact+'.docx'

# Create a new Word document

            


        # Display the details in the Python shell
            print(details_string)

            ff=open(name+"_"+contact+".doc","w")
            ff.write(details_string)
            ff.close()
            # Append to the list for plotting
            percentage_covered_list.append(percentage_covered)

        # Clear previous graph
        self.ax.clear()

        # Plot the graph
        '''
        self.ax.plot(range(1, len(percentage_covered_list) + 1), percentage_covered_list, marker='o', linestyle='-', color='blue')
        self.ax.set_xlabel('Images')
        self.ax.set_ylabel('Percentage of Tumor')
        self.ax.set_title('Tumor Presence Analysis')
        self.ax.set_xticks(range(1, len(percentage_covered_list) + 1))
        self.ax.grid(True)'''

        import matplotlib.pyplot as plt
        import numpy as np
        print(percentage_covered_list)
        #fig, self.ax = plt.subplots()

# Plot the bar chart
        self.ax.bar(range(1, len(percentage_covered_list) + 1), percentage_covered_list, color='blue')

# Set labels and title
        self.ax.set_xlabel(' ')
        self.ax.set_ylabel(' ')
        self.ax.set_title('Tumor Presence Analysis')

# Set x-axis ticks
        self.ax.set_xticks(np.arange(1, len(percentage_covered_list) + 1))

# Display the grid
        self.ax.grid(True)

       
        

    def k_meansClustering(self, image_path, min_contour_area=500):
        image = cv2.imread(image_path)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_white = np.array([0, 0, 200])
        lower_white[2] = min(255, lower_white[2])
        upper_white = np.array([255, 30, 255])
        

        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        total_image_area = image.shape[0] * image.shape[1]
        white_section_area = sum(cv2.contourArea(cnt) for cnt in large_contours)
        percentage_covered = (white_section_area / total_image_area) * 100

        marked_image = image.copy()
        cv2.drawContours(marked_image, large_contours, -1, (0, 255, 0), 2)

        return marked_image, percentage_covered



if __name__ == "__main__":
    root = tk.Tk()

    # Create an instance of the analyzer app
    analyzer_app = WhiteSectionAnalyzerApp(root)
    #app = WhiteSectionAnalyzerApp(root, None)
    # Create an instance of the patient details form and pass the analyzer app instance
    #patient_details_form = PatientDetailsForm(root, analyzer_app)

    root.mainloop()


'''import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WhiteSectionAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("White and Black Section Analyzer")

        # Set background color to black
        self.root.configure(bg="black")

        self.image_paths = []

        self.frame_original = tk.Frame(root, bg="black")
        self.frame_original.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_marked = tk.Frame(root, bg="black")
        self.frame_marked.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas_original = tk.Canvas(self.frame_original, width=400, height=400, bg="black")
        self.canvas_original.pack()

        self.canvas_marked = tk.Canvas(self.frame_marked, width=400, height=400, bg="black")
        self.canvas_marked.pack()

        self.result_label = tk.Label(root, text="", font=('Helvetica', 14), fg="white", bg="black")
        self.result_label.pack(pady=10)

        self.figure, (self.ax_white, self.ax_black) = plt.subplots(nrows=2, figsize=(4, 6))
        self.canvas_graph = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_graph_widget = self.canvas_graph.get_tk_widget()
        self.canvas_graph_widget.pack()

        self.analyze_button = tk.Button(root, text="Browse", command=self.analyze_images, bg="black", fg="white")
        self.analyze_button.pack()

        self.quit_button = tk.Button(root, text="X", command=root.destroy, bg="black", fg="red")
        self.quit_button.pack()

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return ImageTk.PhotoImage(Image.fromarray(image))

    def display_image(self, canvas, image_path):
        image = self.load_image(image_path)
        canvas.config(width=image.width(), height=image.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=image, tags="bg")
        canvas.image = image  # Save reference to avoid garbage collection

    def analyze_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Image(s)", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        white_percentage_list = []
        black_percentage_list = []

        for i, image_path in enumerate(self.image_paths):
            white_percentage, black_percentage = self.analyze_white_and_black_sections(image_path)

            # Display original image
            self.display_image(self.canvas_original, image_path)

            # Display marked image (showing white sections only for simplicity)
            marked_image_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.find_white_sections(image_path), cv2.COLOR_BGR2RGB)))
            self.canvas_marked.config(width=marked_image_tk.width(), height=marked_image_tk.height())
            self.canvas_marked.create_image(0, 0, anchor=tk.NW, image=marked_image_tk)
            self.canvas_marked.image = marked_image_tk  # Save reference to avoid garbage collection

            # Print percentage covered
            result_text = f"Image {i+1}: White - {white_percentage:.2f}%, Black - {black_percentage:.2f}%"
            self.result_label.config(text=result_text)

            # Append to the lists for plotting
            white_percentage_list.append(white_percentage)
            black_percentage_list.append(black_percentage)

        # Clear previous graphs
        self.ax_white.clear()
        self.ax_black.clear()

        # Plot the graphs
        self.ax_white.plot(range(1, len(white_percentage_list) + 1), white_percentage_list, marker='o', linestyle='-', color='blue')
        self.ax_white.set_xlabel('Images')
        self.ax_white.set_ylabel('Percentage of Image Covered by White Sections')
        self.ax_white.set_title('White Section Presence Analysis')
        self.ax_white.set_xticks(range(1, len(white_percentage_list) + 1))
        self.ax_white.grid(True)

        self.ax_black.plot(range(1, len(black_percentage_list) + 1), black_percentage_list, marker='o', linestyle='-', color='red')
        self.ax_black.set_xlabel('Images')
        self.ax_black.set_ylabel('Percentage of Image Covered by Black Sections')
        self.ax_black.set_title('Black Section Presence Analysis')
        self.ax_black.set_xticks(range(1, len(black_percentage_list) + 1))
        self.ax_black.grid(True)

        # Redraw the canvas
        self.canvas_graph.draw()

    def analyze_white_and_black_sections(self, image_path):
        white_percentage = self.find_white_percentage(image_path)
        black_percentage = 100 - white_percentage  # Total area is 100%

        return white_percentage, black_percentage

    def find_white_percentage(self, image_path):
        image = cv2.imread(image_path)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_white = np.array([0, 0, 200])
        upper_white = np.array([255, 30, 255])

        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        total_image_area = image.shape[0] * image.shape[1]
        white_section_area = np.sum(white_mask) / 255  # Counting white pixels
        white_percentage = (white_section_area / total_image_area) * 100

        return white_percentage

    def find_white_sections(self, image_path, min_contour_area=500):
        image = cv2.imread(image_path)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_white = np.array([0, 0, 200])
        upper_white = np.array([255, 30, 255])

        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        marked_image = image.copy()
        cv2.drawContours(marked_image, large_contours, -1, (0, 255, 0), 2)

        return marked_image

if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteSectionAnalyzerApp(root)
    root.mainloop()'''
