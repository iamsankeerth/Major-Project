# # # # import os
# # # # import cv2
# # # # import json
# # # # import pickle
# # # # import numpy as np
# # # # import tensorflow as tf
# # # # import mediapipe as mp
# # # # import tkinter as tk
# # # # from tkinter import ttk, filedialog, messagebox
# # # # from tensorflow.keras.models import load_model
# # # # from PIL import Image, ImageTk, ImageFont, ImageDraw
# # # # import threading
# # # # from datetime import datetime
# # # # import time
# # # # class TamilFingerSpellingGUI:
# # # #     def __init__(self, root):
# # # #         self.root = root
# # # #         self.root.title("Tamil Finger Spelling Recognition")
# # # #         self.root.geometry("1200x800")
# # # #         self.root.configure(bg="#2c3e50")
        
# # # #         # Variables
# # # #         self.model = None
# # # #         self.model_loaded = False
# # # #         self.cap = None
# # # #         self.is_webcam_active = False
# # # #         self.detection_thread = None
# # # #         self.stop_thread = False
# # # #         self.tamil_labels = None
        
# # # #         # Default paths
# # # #         self.default_model_path = "best_lstm_model (3).keras"
# # # #         self.default_labels_path = "tamil_labels.json"
        
# # # #         # MediaPipe setup
# # # #         self.mp_hands = mp.solutions.hands
# # # #         self.mp_drawing = mp.solutions.drawing_utils
# # # #         self.mp_drawing_styles = mp.solutions.drawing_styles
# # # #         self.hands = self.mp_hands.Hands(
# # # #             static_image_mode=False,
# # # #             max_num_hands=2,
# # # #             min_detection_confidence=0.5,
# # # #             min_tracking_confidence=0.5
# # # #         )
        
# # # #         # Create UI elements
# # # #         self.create_widgets()
        
# # # #         # Check for default files
# # # #         self.check_default_files()
        
# # # #     def check_default_files(self):
# # # #         """Check if default model and label files exist and load them"""
# # # #         if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
# # # #             self.model_path_var.set(self.default_model_path)
# # # #             self.labels_path_var.set(self.default_labels_path)
# # # #             self.load_model_and_labels()
        
# # # #     def create_widgets(self):
# # # #         # Main frames layout
# # # #         self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#34495e", 
# # # #                                         sashwidth=4, sashrelief=tk.RAISED)
# # # #         self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
# # # #         # Control frame
# # # #         self.control_frame = tk.Frame(self.main_paned, bg="#34495e", padx=10, pady=10)
        
# # # #         # Display frame
# # # #         self.display_frame = tk.Frame(self.main_paned, bg="#2c3e50", padx=10, pady=10)
        
# # # #         # Add frames to paned window
# # # #         self.main_paned.add(self.control_frame, minsize=300, width=350)
# # # #         self.main_paned.add(self.display_frame, minsize=600)
        
# # # #         # Title and logo
# # # #         title_frame = tk.Frame(self.control_frame, bg="#34495e")
# # # #         title_frame.pack(fill=tk.X, pady=10)
        
# # # #         tk.Label(title_frame, text="Tamil Finger Spelling", 
# # # #                 font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=5)
# # # #         tk.Label(title_frame, text="Recognition System", 
# # # #                 font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
# # # #         # Model and labels loading section
# # # #         files_frame = tk.LabelFrame(self.control_frame, text="Model & Labels", 
# # # #                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # # #         files_frame.pack(fill=tk.X, pady=10)
        
# # # #         # Model path
# # # #         tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
# # # #         self.model_path_var = tk.StringVar()
# # # #         self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
# # # #         self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
# # # #         self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
# # # #                                          bg="#3498db", fg="white", width=6)
# # # #         self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
# # # #         # Labels path
# # # #         tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
# # # #         self.labels_path_var = tk.StringVar()
# # # #         self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
# # # #         self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
# # # #         self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
# # # #                                           bg="#3498db", fg="white", width=6)
# # # #         self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
# # # #         # Load button
# # # #         self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
# # # #                                  command=self.load_model_and_labels,
# # # #                                  bg="#2ecc71", fg="white", width=15, height=2)
# # # #         self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
# # # #         # Input options section
# # # #         input_frame = tk.LabelFrame(self.control_frame, text="Input Options", 
# # # #                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # # #         input_frame.pack(fill=tk.X, pady=10)
        
# # # #         self.image_btn = tk.Button(input_frame, text="Upload Image", command=self.process_image, 
# # # #                                   bg="#e74c3c", fg="white", width=20, height=2, state=tk.DISABLED)
# # # #         self.image_btn.pack(pady=5)
        
# # # #         self.webcam_btn = tk.Button(input_frame, text="Start Webcam", command=self.toggle_webcam, 
# # # #                                    bg="#9b59b6", fg="white", width=20, height=2, state=tk.DISABLED)
# # # #         self.webcam_btn.pack(pady=5)
        
# # # #         self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
# # # #                                     bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
# # # #         self.capture_btn.pack(pady=5)
        
# # # #         # Detection parameters section
# # # #         params_frame = tk.LabelFrame(self.control_frame, text="Detection Parameters", 
# # # #                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # # #         params_frame.pack(fill=tk.X, pady=10)
        
# # # #         tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
# # # #         self.confidence_threshold = tk.DoubleVar(value=0.5)
# # # #         confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
# # # #                                      variable=self.confidence_threshold, 
# # # #                                      orient=tk.HORIZONTAL, length=200)
# # # #         confidence_scale.pack(fill=tk.X, pady=5)
# # # #         tk.Label(params_frame, textvariable=tk.StringVar(value=lambda: f"{self.confidence_threshold.get():.1f}"),
# # # #                 bg="#34495e", fg="white").pack(anchor=tk.E)
        
# # # #         # Results section
# # # #         self.results_frame = tk.LabelFrame(self.control_frame, text="Detection Results", 
# # # #                                           font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # # #         self.results_frame.pack(fill=tk.X, pady=10)
        
# # # #         # Tamil character display
# # # #         self.tamil_char_var = tk.StringVar(value="")
# # # #         self.tamil_char_label = tk.Label(self.results_frame, textvariable=self.tamil_char_var,
# # # #                                         font=("Arial Unicode MS", 60), bg="#34495e", fg="#ecf0f1",
# # # #                                         width=2, height=1)
# # # #         self.tamil_char_label.pack(pady=5)
        
# # # #         # Pronunciation and confidence
# # # #         self.pronunciation_var = tk.StringVar(value="No detection yet")
# # # #         self.pronunciation_label = tk.Label(self.results_frame, textvariable=self.pronunciation_var, 
# # # #                                           font=("Arial", 12), bg="#34495e", fg="white")
# # # #         self.pronunciation_label.pack(pady=5)
        
# # # #         self.confidence_var = tk.StringVar(value="Confidence: 0.00%")
# # # #         self.confidence_label = tk.Label(self.results_frame, textvariable=self.confidence_var, 
# # # #                                         font=("Arial", 10), bg="#34495e", fg="#f1c40f")
# # # #         self.confidence_label.pack(pady=5)
        
# # # #         # History section
# # # #         history_frame = tk.LabelFrame(self.control_frame, text="Detection History", 
# # # #                                      font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # # #         history_frame.pack(fill=tk.X, pady=10)
        
# # # #         self.history_text = tk.Text(history_frame, width=25, height=6, bg="#2c3e50", fg="white",
# # # #                                    font=("Arial", 10))
# # # #         self.history_text.pack(fill=tk.X, pady=5)
# # # #         self.history_text.config(state=tk.DISABLED)
        
# # # #         # Clear button
# # # #         self.clear_btn = tk.Button(history_frame, text="Clear History", 
# # # #                                   command=self.clear_history,
# # # #                                   bg="#7f8c8d", fg="white")
# # # #         self.clear_btn.pack(pady=5)
        
# # # #         # Display frame elements
# # # #         self.canvas = tk.Canvas(self.display_frame, bg="black", width=640, height=480)
# # # #         self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
# # # #         # Reference section
# # # #         reference_frame = tk.LabelFrame(self.display_frame, text="Reference", 
# # # #                                         font=("Arial", 12), bg="#2c3e50", fg="white")
# # # #         reference_frame.pack(fill=tk.X, pady=10)
        
# # # #         # Reference grid (will be populated with character references)
# # # #         self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=100)
# # # #         self.reference_canvas.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
# # # #         # Status bar
# # # #         self.status_var = tk.StringVar(value="Status: Ready")
# # # #         self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
# # # #                                   font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
# # # #                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
# # # #         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
# # # #     def browse_model(self):
# # # #         file_path = filedialog.askopenfilename(filetypes=[
# # # #             ("Keras Model", "*.keras"), 
# # # #             ("H5 Model", "*.h5"),
# # # #             ("All Files", "*.*")
# # # #         ])
# # # #         if file_path:
# # # #             self.model_path_var.set(file_path)
            
# # # #     def browse_labels(self):
# # # #         file_path = filedialog.askopenfilename(filetypes=[
# # # #             ("JSON Files", "*.json"),
# # # #             ("All Files", "*.*")
# # # #         ])
# # # #         if file_path:
# # # #             self.labels_path_var.set(file_path)
            
# # # #     def load_model_and_labels(self):
# # # #         model_path = self.model_path_var.get()
# # # #         labels_path = self.labels_path_var.get()
        
# # # #         if not model_path:
# # # #             messagebox.showerror("Error", "Please select a model file")
# # # #             return
            
# # # #         if not labels_path:
# # # #             messagebox.showerror("Error", "Please select a labels file")
# # # #             return
            
# # # #         if not os.path.exists(model_path):
# # # #             messagebox.showerror("Error", f"Model file not found: {model_path}")
# # # #             return
            
# # # #         if not os.path.exists(labels_path):
# # # #             messagebox.showerror("Error", f"Labels file not found: {labels_path}")
# # # #             return
            
# # # #         try:
# # # #             self.status_var.set("Status: Loading model and labels...")
# # # #             self.root.update()
            
# # # #             # Load the model
# # # #             self.model = load_model(model_path)
            
# # # #             # Load the Tamil labels
# # # #             with open(labels_path, 'r', encoding='utf-8') as f:
# # # #                 self.tamil_labels = json.load(f)
            
# # # #             # Convert string keys to integers
# # # #             self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
# # # #             self.model_loaded = True
            
# # # #             # Enable buttons
# # # #             self.image_btn.config(state=tk.NORMAL)
# # # #             self.webcam_btn.config(state=tk.NORMAL)
            
# # # #             # Update status
# # # #             self.status_var.set("Status: Model and labels loaded successfully")
# # # #             messagebox.showinfo("Success", "Model and labels loaded successfully")
            
# # # #             # Create reference grid
# # # #             self.create_reference_grid()
            
# # # #         except Exception as e:
# # # #             self.status_var.set(f"Status: Error loading model or labels")
# # # #             messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
# # # #     def create_reference_grid(self):
# # # #         """Create a scrollable grid of reference Tamil characters"""
# # # #         # Clear existing content
# # # #         self.reference_canvas.delete("all")
        
# # # #         # Create a frame inside the canvas to hold the characters
# # # #         frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
# # # #         self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
# # # #         # Add characters in a grid (10 per row)
# # # #         row, col = 0, 0
# # # #         for char_id in sorted(self.tamil_labels.keys()):
# # # #             if char_id == 247:  # Skip background class
# # # #                 continue
                
# # # #             # Create frame for each character
# # # #             char_frame = tk.Frame(frame, bg="#34495e", width=50, height=50, 
# # # #                                  padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
# # # #             char_frame.grid(row=row, column=col, padx=2, pady=2)
# # # #             char_frame.grid_propagate(False)  # Keep fixed size
            
# # # #             # Add Tamil character
# # # #             char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
# # # #                                  font=("Arial Unicode MS", 14), bg="#34495e", fg="white")
# # # #             char_label.pack(expand=True)
            
# # # #             # Tooltip with pronunciation
# # # #             self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
# # # #             # Update row and column
# # # #             col += 1
# # # #             if col >= 10:
# # # #                 col = 0
# # # #                 row += 1
        
# # # #         # Update the canvas scroll region
# # # #         frame.update_idletasks()
# # # #         self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
# # # #         # Add scrollbar
# # # #         scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
# # # #                                 command=self.reference_canvas.xview)
# # # #         self.reference_canvas.config(xscrollcommand=scrollbar.set)
# # # #         scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
# # # #     def create_tooltip(self, widget, text):
# # # #         """Create a tooltip for a widget"""
# # # #         def enter(event):
# # # #             # Create a new tooltip window when mouse enters
# # # #             tooltip = tk.Toplevel(widget)
# # # #             tooltip.wm_overrideredirect(True)  # Remove window decorations
            
# # # #             # Create label inside the tooltip window
# # # #             label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
# # # #             label.pack()
            
# # # #             # Position the tooltip near the widget
# # # #             x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
# # # #             x += widget.winfo_rootx() + 25
# # # #             y += widget.winfo_rooty() + 25
# # # #             tooltip.wm_geometry(f"+{x}+{y}")
            
# # # #             # Store the tooltip reference on the widget
# # # #             widget.tooltip = tooltip
            
# # # #         def leave(event):
# # # #             # Destroy the tooltip when mouse leaves
# # # #             if hasattr(widget, 'tooltip'):
# # # #                 widget.tooltip.destroy()
# # # #                 delattr(widget, 'tooltip')
            
# # # #         # Bind events
# # # #         widget.bind("<Enter>", enter)
# # # #         widget.bind("<Leave>", leave)  # Hide initially
                
# # # #     def process_image(self):
# # # #         if not self.model_loaded:
# # # #             messagebox.showerror("Error", "Please load the model and labels first")
# # # #             return
            
# # # #         file_path = filedialog.askopenfilename(filetypes=[
# # # #             ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
# # # #             ("All Files", "*.*")
# # # #         ])
        
# # # #         if not file_path:
# # # #             return
            
# # # #         try:
# # # #             # Read image
# # # #             image = cv2.imread(file_path)
            
# # # #             if image is None:
# # # #                 messagebox.showerror("Error", "Failed to read image")
# # # #                 return
                
# # # #             # Extract keypoints and make prediction
# # # #             result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
# # # #             # Update display
# # # #             self.display_image(result_image)
# # # #             self.update_results(tamil_char, pronunciation, confidence)
# # # #             self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
# # # #             # Add to history
# # # #             self.add_to_history(tamil_char, pronunciation, confidence)
            
# # # #         except Exception as e:
# # # #             self.status_var.set("Status: Error processing image")
# # # #             messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            
# # # #     def toggle_webcam(self):
# # # #         if not self.model_loaded:
# # # #             messagebox.showerror("Error", "Please load the model and labels first")
# # # #             return
            
# # # #         if self.is_webcam_active:
# # # #             # Stop webcam
# # # #             self.stop_thread = True
# # # #             if self.detection_thread:
# # # #                 self.detection_thread.join(timeout=1.0)
# # # #             if self.cap and self.cap.isOpened():
# # # #                 self.cap.release()
# # # #             self.is_webcam_active = False
# # # #             self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
# # # #             self.capture_btn.config(state=tk.DISABLED)
# # # #             self.status_var.set("Status: Webcam stopped")
# # # #         else:
# # # #             # Start webcam
# # # #             self.cap = cv2.VideoCapture(0)
# # # #             if not self.cap.isOpened():
# # # #                 messagebox.showerror("Error", "Failed to open webcam")
# # # #                 return
                
# # # #             self.is_webcam_active = True
# # # #             self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
# # # #             self.capture_btn.config(state=tk.NORMAL)
# # # #             self.status_var.set("Status: Webcam active")
            
# # # #             # Start detection thread
# # # #             self.stop_thread = False
# # # #             self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
# # # #             self.detection_thread.daemon = True
# # # #             self.detection_thread.start()
            
# # # #     def webcam_detection_loop(self):
# # # #         """Process webcam frames and detect Tamil finger spellings"""
# # # #         prev_char = None
# # # #         stability_count = 0
        
# # # #         while not self.stop_thread and self.cap and self.cap.isOpened():
# # # #             try:
# # # #                 ret, frame = self.cap.read()
# # # #                 if not ret:
# # # #                     print("Failed to read from webcam")
# # # #                     break
                    
# # # #                 # Flip the frame horizontally for a more natural view
# # # #                 frame = cv2.flip(frame, 1)
                    
# # # #                 # Extract keypoints and make prediction
# # # #                 result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
# # # #                 # Stability check (to reduce flickering)
# # # #                 if tamil_char == prev_char:
# # # #                     stability_count += 1
# # # #                 else:
# # # #                     stability_count = 0
                    
# # # #                 # Only update the display if prediction is stable or very confident
# # # #                 if stability_count >= 3 or confidence > 80:
# # # #                     # Use a lambda with no parameters to ensure thread-safety
# # # #                     self.root.after(0, lambda f=result_frame: self.display_image(f))
# # # #                     self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
# # # #                                     self.update_results(t, p, c))
                    
# # # #                     # If prediction changes with high confidence, add to history
# # # #                     if tamil_char != prev_char and tamil_char and confidence > 65:
# # # #                         self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
# # # #                                         self.add_to_history(t, p, c))
                        
# # # #                     prev_char = tamil_char
# # # #                 else:
# # # #                     # Just update the display without updating results
# # # #                     self.root.after(0, lambda f=result_frame: self.display_image(f))
                
# # # #                 # # Small delay to reduce CPU usage and make UI more responsive
# # # #                 # time.sleep(0.03)  # Approximate 30 FPS
                
# # # #             except Exception as e:
# # # #                 print(f"Error in webcam loop: {str(e)}")
# # # #                 # time.sleep(0.1)
            
# # # #     def capture_frame(self):
# # # #         if not self.is_webcam_active or not self.cap:
# # # #             return
            
# # # #         ret, frame = self.cap.read()
# # # #         if not ret:
# # # #             messagebox.showerror("Error", "Failed to capture frame")
# # # #             return
            
# # # #         # Save the captured frame
# # # #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# # # #         save_path = f"capture_{timestamp}.jpg"
# # # #         cv2.imwrite(save_path, frame)
        
# # # #         # Process the captured frame
# # # #         result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
# # # #         # Update results
# # # #         self.update_results(tamil_char, pronunciation, confidence)
# # # #         self.add_to_history(tamil_char, pronunciation, confidence)
        
# # # #         # Display notification
# # # #         self.status_var.set(f"Status: Captured frame saved as {save_path}")
# # # #         messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
# # # #     def analyze_image(self, image):
# # # #         """Analyze image and return the recognized Tamil character"""
# # # #         # Extract hand keypoints
# # # #         keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
        
# # # #         if not hands_detected:
# # # #             return annotated_image, "", "No hands detected", 0.0
            
# # # #         # Predict gesture
# # # #         predicted_class, confidence = self.predict_gesture(keypoints)
        
# # # #         # Get Tamil character and pronunciation
# # # #         if predicted_class in self.tamil_labels:
# # # #             tamil_char = self.tamil_labels[predicted_class]["tamil"]
# # # #             pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
# # # #         else:
# # # #             tamil_char = "?"
# # # #             pronunciation = f"Unknown class: {predicted_class}"
        
# # # #         # Add prediction text to image
# # # #         cv2.putText(annotated_image, pronunciation, (10, 30), 
# # # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
# # # #         cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 60), 
# # # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
# # # #         return annotated_image, tamil_char, pronunciation, confidence
            
# # # #     def extract_hand_keypoints(self, image):
# # # #         """Extract hand keypoints using MediaPipe"""
# # # #         # Convert to RGB for MediaPipe
# # # #         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
# # # #         # Process image with MediaPipe
# # # #         results = self.hands.process(image_rgb)
        
# # # #         # Initialize placeholders for hand keypoints
# # # #         left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
# # # #         right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
# # # #         # Make a copy of the image for drawing
# # # #         annotated_image = image.copy()
        
# # # #         # Extract keypoints if hands are detected
# # # #         if results.multi_hand_landmarks:
# # # #             for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
# # # #                 hand_keypoints = []
# # # #                 for landmark in hand_landmarks.landmark:
# # # #                     hand_keypoints.append(landmark.x)
# # # #                     hand_keypoints.append(landmark.y)
                
# # # #                 # Assign to left or right hand (simplified for demonstration)
# # # #                 if hand_idx == 0:
# # # #                     left_hand = hand_keypoints
# # # #                 elif hand_idx == 1:
# # # #                     right_hand = hand_keypoints
                
# # # #                 # Draw landmarks on the image
# # # #                 self.mp_drawing.draw_landmarks(
# # # #                     annotated_image,
# # # #                     hand_landmarks,
# # # #                     self.mp_hands.HAND_CONNECTIONS,
# # # #                     self.mp_drawing_styles.get_default_hand_landmarks_style(),
# # # #                     self.mp_drawing_styles.get_default_hand_connections_style()
# # # #                 )
        
# # # #         # Concatenate left & right hand keypoints
# # # #         data_aux = np.concatenate([left_hand, right_hand])
        
# # # #         return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
# # # #     def predict_gesture(self, keypoints):
# # # #         """Predict the Tamil character gesture"""
# # # #         # Reshape input for LSTM: (samples=1, time steps=1, features=84)
# # # #         input_data = keypoints.reshape(1, 1, 84)
        
# # # #         # Make prediction with the model
# # # #         prediction = self.model.predict(input_data, verbose=0)
        
# # # #         # Get the class with highest probability
# # # #         predicted_class = np.argmax(prediction)
# # # #         confidence = np.max(prediction) * 100
        
# # # #         return predicted_class, confidence
            
# # # #     def display_image(self, image):
# # # #         """Display image on canvas"""
# # # #         try:
# # # #             # Convert OpenCV BGR image to RGB for Tkinter
# # # #             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
# # # #             # Resize to fit canvas if needed
# # # #             canvas_width = self.canvas.winfo_width()
# # # #             canvas_height = self.canvas.winfo_height()
            
# # # #             # If canvas hasn't been fully initialized yet, use default values
# # # #             if canvas_width <= 1 or canvas_height <= 1:
# # # #                 canvas_width = 640  # Default width
# # # #                 canvas_height = 480  # Default height
            
# # # #             # Calculate scaling factor to fit canvas while maintaining aspect ratio
# # # #             img_height, img_width = image_rgb.shape[:2]
# # # #             scale = min(canvas_width/img_width, canvas_height/img_height)
            
# # # #             # New dimensions
# # # #             new_width = int(img_width * scale)
# # # #             new_height = int(img_height * scale)
            
# # # #             # Resize image
# # # #             image_rgb = cv2.resize(image_rgb, (new_width, new_height))
            
# # # #             # Convert to PhotoImage
# # # #             image_pil = Image.fromarray(image_rgb)
# # # #             image_tk = ImageTk.PhotoImage(image=image_pil)
            
# # # #             # Clear previous content and update canvas
# # # #             self.canvas.delete("all")
# # # #             self.canvas.config(width=image_tk.width(), height=image_tk.height())
# # # #             self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
# # # #             self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
# # # #             # Force update to ensure image is displayed
# # # #             self.canvas.update()
            
# # # #         except Exception as e:
# # # #             print(f"Error displaying image: {str(e)}")
        
# # # #     def update_results(self, tamil_char, pronunciation, confidence):
# # # #         """Update the results display"""
# # # #         self.tamil_char_var.set(tamil_char)
# # # #         self.pronunciation_var.set(pronunciation)
# # # #         self.confidence_var.set(f"Confidence: {confidence:.2f}%")
        
# # # #     def add_to_history(self, tamil_char, pronunciation, confidence):
# # # #         """Add detection to history"""
# # # #         if not tamil_char:  # Skip empty detections
# # # #             return
            
# # # #         timestamp = datetime.now().strftime("%H:%M:%S")
# # # #         history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
# # # #         # Enable text widget for editing
# # # #         self.history_text.config(state=tk.NORMAL)
        
# # # #         # Insert at the beginning
# # # #         self.history_text.insert("1.0", history_entry)
        
# # # #         # Limit history length
# # # #         if float(self.history_text.index('end-1c').split('.')[0]) > 20:
# # # #             self.history_text.delete("20.0", tk.END)
            
# # # #         # Disable editing
# # # #         self.history_text.config(state=tk.DISABLED)
        
# # # #     def clear_history(self):
# # # #         """Clear detection history"""
# # # #         self.history_text.config(state=tk.NORMAL)
# # # #         self.history_text.delete("1.0", tk.END)
# # # #         self.history_text.config(state=tk.DISABLED)
        
# # # #     def cleanup(self):
# # # #         """Clean up resources before closing"""
# # # #         if self.cap and self.cap.isOpened():
# # # #             self.cap.release()
# # # #         self.stop_thread = True
# # # #         if self.detection_thread:
# # # #             self.detection_thread.join(timeout=1.0)
# # # #         print("Application closed, resources released")

# # # # def create_tamil_label_mapping():
# # # #     """Create the Tamil character label mapping"""
# # # #     # Check if labels file already exists
# # # #     if os.path.exists("tamil_labels.json"):
# # # #         print("Tamil labels file already exists.")
# # # #         return
        
   

# # # # def main():
# # # #     # Ensure label mapping file exists
# # # #     create_tamil_label_mapping()
    
# # # #     # Create and run the GUI
# # # #     root = tk.Tk()
# # # #     app = TamilFingerSpellingGUI(root)
    
# # # #     # Set up cleanup on exit
# # # #     root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
# # # #     # Start the GUI event loop
# # # #     root.mainloop()

# # # # if __name__ == "__main__":
# # # #     main()

# # # import os
# # # import cv2
# # # import json
# # # import pickle
# # # import numpy as np
# # # import tensorflow as tf
# # # import mediapipe as mp
# # # import tkinter as tk
# # # from tkinter import ttk, filedialog, messagebox
# # # from tkinter import font as tkfont
# # # from tensorflow.keras.models import load_model
# # # from PIL import Image, ImageTk, ImageFont, ImageDraw
# # # import threading
# # # from datetime import datetime
# # # import time
# # # import platform

# # # class TamilFingerSpellingGUI:
# # #     def __init__(self, root):
# # #         self.root = root
# # #         self.root.title("Tamil Finger Spelling Recognition")
# # #         self.root.geometry("1200x800")
# # #         self.root.configure(bg="#2c3e50")
        
# # #         # Variables
# # #         self.model = None
# # #         self.model_loaded = False
# # #         self.cap = None
# # #         self.is_webcam_active = False
# # #         self.detection_thread = None
# # #         self.stop_thread = False
# # #         self.tamil_labels = None
        
# # #         # Setup Tamil fonts
# # #         self.setup_fonts()
        
# # #         # Default paths
# # #         self.default_model_path = "best_lstm_model (3).keras"
# # #         self.default_labels_path = "tamil_labels.json"
        
# # #         # MediaPipe setup
# # #         self.mp_hands = mp.solutions.hands
# # #         self.mp_drawing = mp.solutions.drawing_utils
# # #         self.mp_drawing_styles = mp.solutions.drawing_styles
# # #         self.hands = self.mp_hands.Hands(
# # #             static_image_mode=False,
# # #             max_num_hands=2,
# # #             min_detection_confidence=0.5,
# # #             min_tracking_confidence=0.5
# # #         )
        
# # #         # Create UI elements
# # #         self.create_widgets()
        
# # #         # Check for default files
# # #         self.check_default_files()
        
# # #     def setup_fonts(self):
# # #         """Setup fonts for Tamil display"""
# # #         # Check operating system for appropriate Tamil fonts
# # #         system = platform.system()
        
# # #         if system == "Windows":
# # #             tamil_fonts = ["Latha", "Nirmala UI", "Tamil Sangam MN", "Arial Unicode MS"]
# # #         elif system == "Darwin":  # macOS
# # #             tamil_fonts = ["Tamil Sangam MN", "InaiMathi", "Arial Unicode MS"]
# # #         else:  # Linux and others
# # #             tamil_fonts = ["Noto Sans Tamil", "Lohit Tamil", "FreeSans", "Arial Unicode MS"]
        
# # #         # Find first available Tamil font
# # #         available_fonts = list(tkfont.families())
# # #         self.tamil_font = None
        
# # #         for font_name in tamil_fonts:
# # #             if font_name in available_fonts:
# # #                 self.tamil_font = font_name
# # #                 print(f"Using Tamil font: {font_name}")
# # #                 break
        
# # #         # If no Tamil font found, use a default font and notify user
# # #         if not self.tamil_font:
# # #             self.tamil_font = "TkDefaultFont"
# # #             print("Warning: No Tamil font found. Install a Tamil font for proper display.")
# # #             messagebox.showwarning("Font Warning", 
# # #                 "No Tamil font found. Install a Tamil font like 'Noto Sans Tamil' for proper display.")
    
# # #     def check_default_files(self):
# # #         """Check if default model and label files exist and load them"""
# # #         if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
# # #             self.model_path_var.set(self.default_model_path)
# # #             self.labels_path_var.set(self.default_labels_path)
# # #             self.load_model_and_labels()
        
# # #     def create_widgets(self):
# # #         # Main frames layout
# # #         self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#34495e", 
# # #                                         sashwidth=4, sashrelief=tk.RAISED)
# # #         self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
# # #         # Control frame
# # #         self.control_frame = tk.Frame(self.main_paned, bg="#34495e", padx=10, pady=10)
        
# # #         # Display frame
# # #         self.display_frame = tk.Frame(self.main_paned, bg="#2c3e50", padx=10, pady=10)
        
# # #         # Add frames to paned window
# # #         self.main_paned.add(self.control_frame, minsize=300, width=350)
# # #         self.main_paned.add(self.display_frame, minsize=600)
        
# # #         # Title and logo
# # #         title_frame = tk.Frame(self.control_frame, bg="#34495e")
# # #         title_frame.pack(fill=tk.X, pady=10)
        
# # #         tk.Label(title_frame, text="Tamil Finger Spelling", 
# # #                 font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=5)
# # #         tk.Label(title_frame, text="Recognition System", 
# # #                 font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
# # #         # Model and labels loading section
# # #         files_frame = tk.LabelFrame(self.control_frame, text="Model & Labels", 
# # #                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # #         files_frame.pack(fill=tk.X, pady=10)
        
# # #         # Model path
# # #         tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
# # #         self.model_path_var = tk.StringVar()
# # #         self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
# # #         self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
# # #         self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
# # #                                          bg="#3498db", fg="white", width=6)
# # #         self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
# # #         # Labels path
# # #         tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
# # #         self.labels_path_var = tk.StringVar()
# # #         self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
# # #         self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
# # #         self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
# # #                                           bg="#3498db", fg="white", width=6)
# # #         self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
# # #         # Load button
# # #         self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
# # #                                  command=self.load_model_and_labels,
# # #                                  bg="#2ecc71", fg="white", width=15, height=2)
# # #         self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
# # #         # Input options section
# # #         input_frame = tk.LabelFrame(self.control_frame, text="Input Options", 
# # #                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # #         input_frame.pack(fill=tk.X, pady=10)
        
# # #         self.image_btn = tk.Button(input_frame, text="Upload Image", command=self.process_image, 
# # #                                   bg="#e74c3c", fg="white", width=20, height=2, state=tk.DISABLED)
# # #         self.image_btn.pack(pady=5)
        
# # #         self.webcam_btn = tk.Button(input_frame, text="Start Webcam", command=self.toggle_webcam, 
# # #                                    bg="#9b59b6", fg="white", width=20, height=2, state=tk.DISABLED)
# # #         self.webcam_btn.pack(pady=5)
        
# # #         self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
# # #                                     bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
# # #         self.capture_btn.pack(pady=5)
        
# # #         # Detection parameters section
# # #         params_frame = tk.LabelFrame(self.control_frame, text="Detection Parameters", 
# # #                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # #         params_frame.pack(fill=tk.X, pady=10)
        
# # #         tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
# # #         self.confidence_threshold = tk.DoubleVar(value=0.5)
# # #         confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
# # #                                      variable=self.confidence_threshold, 
# # #                                      orient=tk.HORIZONTAL, length=200)
# # #         confidence_scale.pack(fill=tk.X, pady=5)
        
# # #         # Create a label to display the current value
# # #         self.threshold_value_label = tk.Label(params_frame, text="0.5", bg="#34495e", fg="white")
# # #         self.threshold_value_label.pack(anchor=tk.E)
        
# # #         # Update label when scale changes
# # #         confidence_scale.bind("<Motion>", self.update_threshold_label)
        
# # #         # Enhanced results frame with better Tamil character display
# # #         self.enhance_results_frame()
        
# # #         # History section
# # #         history_frame = tk.LabelFrame(self.control_frame, text="Detection History", 
# # #                                      font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# # #         history_frame.pack(fill=tk.X, pady=10)
        
# # #         self.history_text = tk.Text(history_frame, width=25, height=6, bg="#2c3e50", fg="white",
# # #                                    font=("Arial", 10))
# # #         self.history_text.pack(fill=tk.X, pady=5)
# # #         self.history_text.config(state=tk.DISABLED)
        
# # #         # Clear button
# # #         self.clear_btn = tk.Button(history_frame, text="Clear History", 
# # #                                   command=self.clear_history,
# # #                                   bg="#7f8c8d", fg="white")
# # #         self.clear_btn.pack(pady=5)
        
# # #         # Display frame elements
# # #         self.canvas = tk.Canvas(self.display_frame, bg="black", width=640, height=480)
# # #         self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
# # #         # Reference section
# # #         reference_frame = tk.LabelFrame(self.display_frame, text="Reference", 
# # #                                         font=("Arial", 12), bg="#2c3e50", fg="white")
# # #         reference_frame.pack(fill=tk.X, pady=10)
        
# # #         # Reference grid (will be populated with character references)
# # #         self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=100)
# # #         self.reference_canvas.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
# # #         # Status bar
# # #         self.status_var = tk.StringVar(value="Status: Ready")
# # #         self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
# # #                                   font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
# # #                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
# # #         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
# # #     def enhance_results_frame(self):
# # #         """Enhanced results frame with better Tamil character display"""
# # #         # Results section with improved visibility
# # #         self.results_frame = tk.LabelFrame(self.control_frame, text="Detection Results", 
# # #                                           font=("Arial", 14, "bold"), bg="#34495e", fg="white", 
# # #                                           padx=10, pady=10)
# # #         self.results_frame.pack(fill=tk.X, pady=10)
        
# # #         # Create a frame with a distinct background for the Tamil character
# # #         char_display_frame = tk.Frame(self.results_frame, bg="#2c3e50", 
# # #                                      padx=10, pady=10, relief=tk.RAISED, bd=2)
# # #         char_display_frame.pack(fill=tk.X, pady=5)
        
# # #         # Tamil character display - much larger
# # #         self.tamil_char_var = tk.StringVar(value="")
# # #         self.tamil_char_label = tk.Label(char_display_frame, textvariable=self.tamil_char_var,
# # #                                         font=(self.tamil_font, 100), bg="#2c3e50", fg="#ecf0f1")
# # #         self.tamil_char_label.pack(pady=5)
        
# # #         # Pronunciation with better formatting
# # #         pronunciation_frame = tk.Frame(self.results_frame, bg="#34495e")
# # #         pronunciation_frame.pack(fill=tk.X, pady=5)
        
# # #         tk.Label(pronunciation_frame, text="Pronunciation:", 
# # #                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
# # #         self.pronunciation_var = tk.StringVar(value="No detection yet")
# # #         self.pronunciation_label = tk.Label(pronunciation_frame, textvariable=self.pronunciation_var, 
# # #                                           font=("Arial", 12), bg="#34495e", fg="white")
# # #         self.pronunciation_label.pack(side=tk.LEFT, padx=5)
        
# # #         # Confidence with progress bar
# # #         confidence_frame = tk.Frame(self.results_frame, bg="#34495e")
# # #         confidence_frame.pack(fill=tk.X, pady=5)
        
# # #         tk.Label(confidence_frame, text="Confidence:", 
# # #                 font=("Arial", 10, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
# # #         self.confidence_var = tk.StringVar(value="0.00%")
# # #         self.confidence_label = tk.Label(confidence_frame, textvariable=self.confidence_var, 
# # #                                         font=("Arial", 10), bg="#34495e", fg="white")
# # #         self.confidence_label.pack(side=tk.LEFT, padx=5)
        
# # #         # Add a simple progress bar for confidence
# # #         self.confidence_progress_frame = tk.Frame(self.results_frame, bg="#34495e", height=20)
# # #         self.confidence_progress_frame.pack(fill=tk.X, pady=5)
        
# # #         self.confidence_progress = tk.Canvas(self.confidence_progress_frame, 
# # #                                             bg="#2c3e50", height=20, bd=0, highlightthickness=0)
# # #         self.confidence_progress.pack(fill=tk.X)
    
# # #     def update_threshold_label(self, event=None):
# # #         """Update the threshold value label"""
# # #         self.threshold_value_label.config(text=f"{self.confidence_threshold.get():.1f}")
        
# # #     def browse_model(self):
# # #         file_path = filedialog.askopenfilename(filetypes=[
# # #             ("Keras Model", "*.keras"), 
# # #             ("H5 Model", "*.h5"),
# # #             ("All Files", "*.*")
# # #         ])
# # #         if file_path:
# # #             self.model_path_var.set(file_path)
            
# # #     def browse_labels(self):
# # #         file_path = filedialog.askopenfilename(filetypes=[
# # #             ("JSON Files", "*.json"),
# # #             ("All Files", "*.*")
# # #         ])
# # #         if file_path:
# # #             self.labels_path_var.set(file_path)
            
# # #     def load_model_and_labels(self):
# # #         model_path = self.model_path_var.get()
# # #         labels_path = self.labels_path_var.get()
        
# # #         if not model_path:
# # #             messagebox.showerror("Error", "Please select a model file")
# # #             return
            
# # #         if not labels_path:
# # #             messagebox.showerror("Error", "Please select a labels file")
# # #             return
            
# # #         if not os.path.exists(model_path):
# # #             messagebox.showerror("Error", f"Model file not found: {model_path}")
# # #             return
            
# # #         if not os.path.exists(labels_path):
# # #             messagebox.showerror("Error", f"Labels file not found: {labels_path}")
# # #             return
            
# # #         try:
# # #             self.status_var.set("Status: Loading model and labels...")
# # #             self.root.update()
            
# # #             # Load the model
# # #             self.model = load_model(model_path)
            
# # #             # Load the Tamil labels
# # #             with open(labels_path, 'r', encoding='utf-8') as f:
# # #                 self.tamil_labels = json.load(f)
            
# # #             # Convert string keys to integers
# # #             self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
# # #             self.model_loaded = True
            
# # #             # Enable buttons
# # #             self.image_btn.config(state=tk.NORMAL)
# # #             self.webcam_btn.config(state=tk.NORMAL)
            
# # #             # Update status
# # #             self.status_var.set("Status: Model and labels loaded successfully")
# # #             messagebox.showinfo("Success", "Model and labels loaded successfully")
            
# # #             # Create reference grid
# # #             self.create_reference_grid()
            
# # #         except Exception as e:
# # #             self.status_var.set(f"Status: Error loading model or labels")
# # #             messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
# # #     def create_reference_grid(self):
# # #         """Create a scrollable grid of reference Tamil characters"""
# # #         # Clear existing content
# # #         self.reference_canvas.delete("all")
        
# # #         # Create a frame inside the canvas to hold the characters
# # #         frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
# # #         self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
# # #         # Add characters in a grid (10 per row)
# # #         row, col = 0, 0
# # #         self.reference_labels = {}  # Store references to labels for highlighting
        
# # #         for char_id in sorted(self.tamil_labels.keys()):
# # #             if char_id == 247:  # Skip background class (if applicable)
# # #                 continue
                
# # #             # Create frame for each character
# # #             char_frame = tk.Frame(frame, bg="#34495e", width=60, height=60, 
# # #                                  padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
# # #             char_frame.grid(row=row, column=col, padx=3, pady=3)
# # #             char_frame.grid_propagate(False)  # Keep fixed size
            
# # #             # Add Tamil character with improved font
# # #             char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
# # #                                  font=(self.tamil_font, 16), bg="#34495e", fg="white")
# # #             char_label.pack(expand=True)
            
# # #             # Store reference to this label
# # #             self.reference_labels[self.tamil_labels[char_id]["tamil"]] = char_label
            
# # #             # Tooltip with pronunciation
# # #             self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
# # #             # Update row and column
# # #             col += 1
# # #             if col >= 10:
# # #                 col = 0
# # #                 row += 1
        
# # #         # Update the canvas scroll region
# # #         frame.update_idletasks()
# # #         self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
# # #         # Add scrollbar
# # #         scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
# # #                                 command=self.reference_canvas.xview)
# # #         self.reference_canvas.config(xscrollcommand=scrollbar.set)
# # #         scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
# # #     def create_tooltip(self, widget, text):
# # #         """Create a tooltip for a widget"""
# # #         def enter(event):
# # #             # Create a new tooltip window when mouse enters
# # #             tooltip = tk.Toplevel(widget)
# # #             tooltip.wm_overrideredirect(True)  # Remove window decorations
            
# # #             # Create label inside the tooltip window
# # #             label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
# # #             label.pack()
            
# # #             # Position the tooltip near the widget
# # #             x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
# # #             x += widget.winfo_rootx() + 25
# # #             y += widget.winfo_rooty() + 25
# # #             tooltip.wm_geometry(f"+{x}+{y}")
            
# # #             # Store the tooltip reference on the widget
# # #             widget.tooltip = tooltip
            
# # #         def leave(event):
# # #             # Destroy the tooltip when mouse leaves
# # #             if hasattr(widget, 'tooltip'):
# # #                 widget.tooltip.destroy()
# # #                 delattr(widget, 'tooltip')
            
# # #         # Bind events
# # #         widget.bind("<Enter>", enter)
# # #         widget.bind("<Leave>", leave)
    
# # #     def process_image(self):
# # #         if not self.model_loaded:
# # #             messagebox.showerror("Error", "Please load the model and labels first")
# # #             return
            
# # #         file_path = filedialog.askopenfilename(filetypes=[
# # #             ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
# # #             ("All Files", "*.*")
# # #         ])
        
# # #         if not file_path:
# # #             return
            
# # #         try:
# # #             # Read image
# # #             image = cv2.imread(file_path)
            
# # #             if image is None:
# # #                 messagebox.showerror("Error", "Failed to read image")
# # #                 return
                
# # #             # Update status while processing
# # #             self.status_var.set(f"Status: Processing image {os.path.basename(file_path)}...")
# # #             self.root.update()
            
# # #             # Extract keypoints and make prediction
# # #             result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
# # #             # Save a copy of the processed image for debugging (optional)
# # #             debug_path = f"debug_{os.path.basename(file_path)}"
# # #             cv2.imwrite(debug_path, result_image)
            
# # #             # Update display - make sure image is shown
# # #             self.display_image(result_image)
# # #             self.update_results(tamil_char, pronunciation, confidence)
# # #             self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
# # #             # Add to history
# # #             self.add_to_history(tamil_char, pronunciation, confidence)
            
# # #         except Exception as e:
# # #             self.status_var.set("Status: Error processing image")
# # #             error_msg = f"Failed to process image: {str(e)}"
# # #             print(error_msg)  # Print to console for debugging
# # #             messagebox.showerror("Error", error_msg)
                
# # #     def toggle_webcam(self):
# # #         if not self.model_loaded:
# # #             messagebox.showerror("Error", "Please load the model and labels first")
# # #             return
            
# # #         if self.is_webcam_active:
# # #             # Stop webcam
# # #             self.stop_thread = True
# # #             if self.detection_thread:
# # #                 self.detection_thread.join(timeout=1.0)
# # #             if self.cap and self.cap.isOpened():
# # #                 self.cap.release()
# # #             self.is_webcam_active = False
# # #             self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
# # #             self.capture_btn.config(state=tk.DISABLED)
# # #             self.status_var.set("Status: Webcam stopped")
# # #         else:
# # #             # Start webcam
# # #             self.cap = cv2.VideoCapture(0)
# # #             if not self.cap.isOpened():
# # #                 messagebox.showerror("Error", "Failed to open webcam")
# # #                 return
                
# # #             self.is_webcam_active = True
# # #             self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
# # #             self.capture_btn.config(state=tk.NORMAL)
# # #             self.status_var.set("Status: Webcam active")
            
# # #             # Start detection thread
# # #             self.stop_thread = False
# # #             self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
# # #             self.detection_thread.daemon = True
# # #             self.detection_thread.start()
            
# # #     def webcam_detection_loop(self):
# # #         """Process webcam frames and detect Tamil finger spellings"""
# # #         prev_char = None
# # #         stability_count = 0
        
# # #         while not self.stop_thread and self.cap and self.cap.isOpened():
# # #             try:
# # #                 ret, frame = self.cap.read()
# # #                 if not ret:
# # #                     print("Failed to read from webcam")
# # #                     break
                    
# # #                 # Flip the frame horizontally for a more natural view
# # #                 frame = cv2.flip(frame, 1)
                    
# # #                 # Extract keypoints and make prediction
# # #                 result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
# # #                 # Stability check (to reduce flickering)
# # #                 if tamil_char == prev_char:
# # #                     stability_count += 1
# # #                 else:
# # #                     stability_count = 0
                    
# # #                 # Only update the display if prediction is stable or very confident
# # #                 if stability_count >= 3 or confidence > 80:
# # #                     # Use a lambda with no parameters to ensure thread-safety
# # #                     self.root.after(0, lambda f=result_frame: self.display_image(f))
# # #                     self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
# # #                                     self.update_results(t, p, c))
                    
# # #                     # If prediction changes with high confidence, add to history
# # #                     if tamil_char != prev_char and tamil_char and confidence > 65:
# # #                         self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
# # #                                         self.add_to_history(t, p, c))
                        
# # #                     prev_char = tamil_char
# # #                 else:
# # #                     # Just update the display without updating results
# # #                     self.root.after(0, lambda f=result_frame: self.display_image(f))
                
# # #                 # Small delay to reduce CPU usage and make UI more responsive
# # #                 time.sleep(0.03)  # Approximate 30 FPS
                
# # #             except Exception as e:
# # #                 print(f"Error in webcam loop: {str(e)}")
# # #                 time.sleep(0.1)
            
# # #     def capture_frame(self):
# # #         if not self.is_webcam_active or not self.cap:
# # #             return
            
# # #         ret, frame = self.cap.read()
# # #         if not ret:
# # #             messagebox.showerror("Error", "Failed to capture frame")
# # #             return
            
# # #         # Flip the frame horizontally for a more natural view
# # #         frame = cv2.flip(frame, 1)
        
# # #         # Save the captured frame
# # #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# # #         save_path = f"capture_{timestamp}.jpg"
# # #         cv2.imwrite(save_path, frame)
        
# # #         # Process the captured frame
# # #         result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
# # #         # Update results
# # #         self.update_results(tamil_char, pronunciation, confidence)
# # #         self.add_to_history(tamil_char, pronunciation, confidence)
        
# # #         # Display notification
# # #         self.status_var.set(f"Status: Captured frame saved as {save_path}")
# # #         messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
# # #     def analyze_image(self, image):
# # #         """Analyze image and return the recognized Tamil character"""
# # #         # Extract hand keypoints
# # #         keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
        
# # #         if not hands_detected:
# # #             return annotated_image, "", "No hands detected", 0.0
            
# # #         # Predict gesture
# # #         predicted_class, confidence = self.predict_gesture(keypoints)
        
# # #         # Get Tamil character and pronunciation
# # #         if predicted_class in self.tamil_labels:
# # #             tamil_char = self.tamil_labels[predicted_class]["tamil"]
# # #             pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
# # #         else:
# # #             tamil_char = "?"
# # #             pronunciation = f"Unknown class: {predicted_class}"
        
# # #         # Add prediction text to image
# # #         cv2.putText(annotated_image, pronunciation, (10, 30), 
# # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
# # #         cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 60), 
# # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
# # #         return annotated_image, tamil_char, pronunciation, confidence
            
# # #     def extract_hand_keypoints(self, image):
# # #         """Extract hand keypoints using MediaPipe"""
# # #         # Convert to RGB for MediaPipe
# # #         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
# # #         # Process image with MediaPipe
# # #         results = self.hands.process(image_rgb)
        
# # #         # Initialize placeholders for hand keypoints
# # #         left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
# # #         right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
# # #         # Make a copy of the image for drawing
# # #         annotated_image = image.copy()
        
# # #         # Extract keypoints if hands are detected
# # #         if results.multi_hand_landmarks:
# # #             for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
# # #                 hand_keypoints = []
# # #                 for landmark in hand_landmarks.landmark:
# # #                     hand_keypoints.append(landmark.x)
# # #                     hand_keypoints.append(landmark.y)
                
# # #                 # Assign to left or right hand (simplified for demonstration)
# # #                 if hand_idx == 0:
# # #                     left_hand = hand_keypoints
# # #                 elif hand_idx == 1:
# # #                     right_hand = hand_keypoints
                
# # #                 # Draw landmarks on the image
# # #                 self.mp_drawing.draw_landmarks(
# # #                     annotated_image,
# # #                     hand_landmarks,
# # #                     self.mp_hands.HAND_CONNECTIONS,
# # #                     self.mp_drawing_styles.get_default_hand_landmarks_style(),
# # #                     self.mp_drawing_styles.get_default_hand_connections_style()
# # #                 )
        
# # #         # Concatenate left & right hand keypoints
# # #         data_aux = np.concatenate([left_hand, right_hand])
        
# # #         return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
# # #     def predict_gesture(self, keypoints):
# # #         """Predict the Tamil character gesture"""
# # #         # Reshape input for LSTM: (samples=1, time steps=1, features=84)
# # #         input_data = keypoints.reshape(1, 1, 84)
        
# # #         # Make prediction with the model
# # #         prediction = self.model.predict(input_data, verbose=0)
        
# # #         # Get the class with highest probability
# # #         predicted_class = np.argmax(prediction)
# # #         confidence = np.max(prediction) * 100
        
# # #         return predicted_class, confidence
            
# # #     def display_image(self, image):
# # #         """Display image on canvas with proper scaling"""
# # #         try:
# # #             # Convert OpenCV BGR image to RGB for Tkinter
# # #             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
# # #             # Get canvas dimensions
# # #             canvas_width = self.canvas.winfo_width()
# # #             canvas_height = self.canvas.winfo_height()
            
# # #             # If canvas hasn't been fully initialized yet, use default values
# # #             if canvas_width <= 1 or canvas_height <= 1:
# # #                 canvas_width = 640  # Default width
# # #                 canvas_height = 480  # Default height
            
# # #             # Calculate scaling factor to fit canvas while maintaining aspect ratio
# # #             img_height, img_width = image_rgb.shape[:2]
# # #             scale = min(canvas_width/img_width, canvas_height/img_height)
            
# # #             # New dimensions
# # #             new_width = int(img_width * scale)
# # #             new_height = int(img_height * scale)
            
# # #             # Resize image
# # #             if scale != 1.0:  # Only resize if needed
# # #                 image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
# # #                                       interpolation=cv2.INTER_AREA)
            
# # #             # Convert to PhotoImage
# # #             image_pil = Image.fromarray(image_rgb)
# # #             image_tk = ImageTk.PhotoImage(image=image_pil)
            
# # #             # Clear previous content and update canvas
# # #             self.canvas.delete("all")
            
# # #             # Center the image on the canvas
# # #             x_offset = max(0, (canvas_width - new_width) // 2)
# # #             y_offset = max(0, (canvas_height - new_height) // 2)
            
# # #             # Draw a border around the image area
# # #             self.canvas.create_rectangle(
# # #                 x_offset-2, y_offset-2, 
# # #                 x_offset+new_width+2, y_offset+new_height+2,
# # #                 outline="#3498db", width=2
# # #             )
            
# # #             # Create image
# # #             self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
# # #             self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
# # #             # Force update to ensure image is displayed
# # #             self.canvas.update()
            
# # #             # Print debug info
# # #             print(f"Displaying image: original size={img_width}x{img_height}, "
# # #                   f"scaled size={new_width}x{new_height}, canvas size={canvas_width}x{canvas_height}")
            
# # #         except Exception as e:
# # #             print(f"Error displaying image: {str(e)}")
        
# # #     def update_results(self, tamil_char, pronunciation, confidence):
# # #         """Update the results display with enhanced visuals"""
# # #         self.tamil_char_var.set(tamil_char)
# # #         self.pronunciation_var.set(pronunciation)
# # #         self.confidence_var.set(f"{confidence:.2f}%")
# # #         self.update_confidence_progress(confidence)
        
# # #         # Highlight the detected character in the reference grid
# # #         self.highlight_reference_character(tamil_char)

# # #     def update_confidence_progress(self, confidence):
# # #         """Update the confidence progress bar"""
# # #         self.confidence_progress.delete("all")
# # #         width = self.confidence_progress.winfo_width()
# # #         if width < 10:  # Not yet properly initialized
# # #             width = 200
        
# # #         # Draw the background
# # #         self.confidence_progress.create_rectangle(0, 0, width, 20, fill="#2c3e50", outline="")
        
# # #         # Draw the progress bar
# # #         progress_width = int(width * confidence / 100)
        
# # #         # Color based on confidence level
# # #         if confidence < 30:
# # #             color = "#e74c3c"  # Red for low confidence
# # #         elif confidence < 70:
# # #             color = "#f39c12"  # Orange for medium confidence
# # #         else:
# # #             color = "#2ecc71"  # Green for high confidence
        
# # #         self.confidence_progress.create_rectangle(0, 0, progress_width, 20, 
# # #                                                  fill=color, outline="")
        
# # #         # Add text
# # #         self.confidence_progress.create_text(width/2, 10, 
# # #                                             text=f"{confidence:.2f}%", 
# # #                                             fill="white", font=("Arial", 9, "bold"))
    
# # #     def highlight_reference_character(self, tamil_char):
# # #         """Highlight the detected character in the reference grid"""
# # #         # Reset all characters to normal background
# # #         for label in self.reference_labels.values():
# # #             label.config(bg="#34495e")
        
# # #         # Highlight the detected character if it exists in our reference grid
# # #         if tamil_char in self.reference_labels:
# # #             self.reference_labels[tamil_char].config(bg="#e74c3c")  # Highlight with a red background
        
# # #     def add_to_history(self, tamil_char, pronunciation, confidence):
# # #         """Add detection to history"""
# # #         if not tamil_char:  # Skip empty detections
# # #             return
            
# # #         timestamp = datetime.now().strftime("%H:%M:%S")
# # #         history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
# # #         # Enable text widget for editing
# # #         self.history_text.config(state=tk.NORMAL)
        
# # #         # Insert at the beginning
# # #         self.history_text.insert("1.0", history_entry)
        
# # #         # Limit history length
# # #         if float(self.history_text.index('end-1c').split('.')[0]) > 20:
# # #             self.history_text.delete("20.0", tk.END)
            
# # #         # Disable editing
# # #         self.history_text.config(state=tk.DISABLED)
        
# # #     def clear_history(self):
# # #         """Clear detection history"""
# # #         self.history_text.config(state=tk.NORMAL)
# # #         self.history_text.delete("1.0", tk.END)
# # #         self.history_text.config(state=tk.DISABLED)
        
# # #     def cleanup(self):
# # #         """Clean up resources before closing"""
# # #         if self.cap and self.cap.isOpened():
# # #             self.cap.release()
# # #         self.stop_thread = True
# # #         if self.detection_thread:
# # #             self.detection_thread.join(timeout=1.0)
# # #         print("Application closed, resources released")

# # # def create_tamil_label_mapping():
# # #     """Create the Tamil character label mapping"""
# # #     # Check if labels file already exists
# # #     if os.path.exists("tamil_labels.json"):
# # #         print("Tamil labels file already exists.")
# # #         return
    
# # #     # If we needed to create a default Tamil labels file,
# # #     # we would add that code here. For now, we'll assume
# # #     # the file is provided by the user.
# # #     print("Tamil labels file not found. Please provide a valid labels file.")

# # # def main():
# # #     # Ensure label mapping file exists
# # #     create_tamil_label_mapping()
    
# # #     # Create and run the GUI
# # #     root = tk.Tk()
# # #     app = TamilFingerSpellingGUI(root)
    
# # #     # Set up cleanup on exit
# # #     root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
# # #     # Start the GUI event loop
# # #     root.mainloop()

# # # if __name__ == "__main__":
# # #     main()
# # import os
# # import cv2
# # import json
# # import pickle
# # import numpy as np
# # import tensorflow as tf
# # import mediapipe as mp
# # import tkinter as tk
# # from tkinter import ttk, filedialog, messagebox
# # from tkinter import font as tkfont
# # from tensorflow.keras.models import load_model
# # from PIL import Image, ImageTk, ImageFont, ImageDraw
# # import threading
# # from datetime import datetime
# # import time
# # import platform

# # class TamilFingerSpellingGUI:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Tamil Finger Spelling Recognition")
# #         self.root.geometry("1200x800")
# #         self.root.configure(bg="#2c3e50")
        
# #         # Variables
# #         self.model = None
# #         self.model_loaded = False
# #         self.cap = None
# #         self.is_webcam_active = False
# #         self.detection_thread = None
# #         self.stop_thread = False
# #         self.tamil_labels = None
        
# #         # Setup Tamil fonts
# #         self.setup_fonts()
        
# #         # Default paths
# #         self.default_model_path = "best_lstm_model (3).keras"
# #         self.default_labels_path = "tamil_labels.json"
        
# #         # MediaPipe setup
# #         self.mp_hands = mp.solutions.hands
# #         self.mp_drawing = mp.solutions.drawing_utils
# #         self.mp_drawing_styles = mp.solutions.drawing_styles
# #         self.hands = self.mp_hands.Hands(
# #             static_image_mode=False,
# #             max_num_hands=2,
# #             min_detection_confidence=0.5,
# #             min_tracking_confidence=0.5
# #         )
        
# #         # Create UI elements
# #         self.create_widgets()
        
# #         # Check for default files
# #         self.check_default_files()
        
# #     def setup_fonts(self):
# #         """Setup fonts for Tamil display"""
# #         # Check operating system for appropriate Tamil fonts
# #         system = platform.system()
        
# #         if system == "Windows":
# #             tamil_fonts = ["Latha", "Nirmala UI", "Tamil Sangam MN", "Arial Unicode MS"]
# #         elif system == "Darwin":  # macOS
# #             tamil_fonts = ["Tamil Sangam MN", "InaiMathi", "Arial Unicode MS"]
# #         else:  # Linux and others
# #             tamil_fonts = ["Noto Sans Tamil", "Lohit Tamil", "FreeSans", "Arial Unicode MS"]
        
# #         # Find first available Tamil font
# #         available_fonts = list(tkfont.families())
# #         self.tamil_font = None
        
# #         for font_name in tamil_fonts:
# #             if font_name in available_fonts:
# #                 self.tamil_font = font_name
# #                 print(f"Using Tamil font: {font_name}")
# #                 break
        
# #         # If no Tamil font found, use a default font and notify user
# #         if not self.tamil_font:
# #             self.tamil_font = "TkDefaultFont"
# #             print("Warning: No Tamil font found. Install a Tamil font for proper display.")
# #             messagebox.showwarning("Font Warning", 
# #                 "No Tamil font found. Install a Tamil font like 'Noto Sans Tamil' for proper display.")
    
# #     def check_default_files(self):
# #         """Check if default model and label files exist and load them"""
# #         if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
# #             self.model_path_var.set(self.default_model_path)
# #             self.labels_path_var.set(self.default_labels_path)
# #             self.load_model_and_labels()
        
# #     def create_widgets(self):
# #         # Main frames layout - ADJUSTED: give more space to control frame for larger results
# #         self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#34495e", 
# #                                         sashwidth=4, sashrelief=tk.RAISED)
# #         self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
# #         # Control frame
# #         self.control_frame = tk.Frame(self.main_paned, bg="#34495e", padx=10, pady=10)
        
# #         # Display frame
# #         self.display_frame = tk.Frame(self.main_paned, bg="#2c3e50", padx=10, pady=10)
        
# #         # Add frames to paned window - ADJUSTED: increase minimum width of control frame
# #         self.main_paned.add(self.control_frame, minsize=400, width=450)
# #         self.main_paned.add(self.display_frame, minsize=600)
        
# #         # Title and logo
# #         title_frame = tk.Frame(self.control_frame, bg="#34495e")
# #         title_frame.pack(fill=tk.X, pady=10)
        
# #         tk.Label(title_frame, text="Tamil Finger Spelling", 
# #                 font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=5)
# #         tk.Label(title_frame, text="Recognition System", 
# #                 font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
# #         # Enhanced results frame with MUCH larger Tamil character display
# #         # MOVED UP in the hierarchy to make it more prominent
# #         self.enhance_results_frame()
        
# #         # Model and labels loading section
# #         files_frame = tk.LabelFrame(self.control_frame, text="Model & Labels", 
# #                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# #         files_frame.pack(fill=tk.X, pady=10)
        
# #         # Model path
# #         tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
# #         self.model_path_var = tk.StringVar()
# #         self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
# #         self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
# #         self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
# #                                          bg="#3498db", fg="white", width=6)
# #         self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
# #         # Labels path
# #         tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
# #         self.labels_path_var = tk.StringVar()
# #         self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
# #         self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
# #         self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
# #                                           bg="#3498db", fg="white", width=6)
# #         self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
# #         # Load button
# #         self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
# #                                  command=self.load_model_and_labels,
# #                                  bg="#2ecc71", fg="white", width=15, height=2)
# #         self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
# #         # Input options section
# #         input_frame = tk.LabelFrame(self.control_frame, text="Input Options", 
# #                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# #         input_frame.pack(fill=tk.X, pady=10)
        
# #         self.image_btn = tk.Button(input_frame, text="Upload Image", command=self.process_image, 
# #                                   bg="#e74c3c", fg="white", width=20, height=2, state=tk.DISABLED)
# #         self.image_btn.pack(pady=5)
        
# #         self.webcam_btn = tk.Button(input_frame, text="Start Webcam", command=self.toggle_webcam, 
# #                                    bg="#9b59b6", fg="white", width=20, height=2, state=tk.DISABLED)
# #         self.webcam_btn.pack(pady=5)
        
# #         self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
# #                                     bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
# #         self.capture_btn.pack(pady=5)
        
# #         # Detection parameters section
# #         params_frame = tk.LabelFrame(self.control_frame, text="Detection Parameters", 
# #                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# #         params_frame.pack(fill=tk.X, pady=10)
        
# #         tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
# #         self.confidence_threshold = tk.DoubleVar(value=0.5)
# #         confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
# #                                      variable=self.confidence_threshold, 
# #                                      orient=tk.HORIZONTAL, length=200)
# #         confidence_scale.pack(fill=tk.X, pady=5)
        
# #         # Create a label to display the current value
# #         self.threshold_value_label = tk.Label(params_frame, text="0.5", bg="#34495e", fg="white")
# #         self.threshold_value_label.pack(anchor=tk.E)
        
# #         # Update label when scale changes
# #         confidence_scale.bind("<Motion>", self.update_threshold_label)
        
# #         # History section
# #         history_frame = tk.LabelFrame(self.control_frame, text="Detection History", 
# #                                      font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
# #         history_frame.pack(fill=tk.X, pady=10)
        
# #         self.history_text = tk.Text(history_frame, width=25, height=6, bg="#2c3e50", fg="white",
# #                                    font=("Arial", 10))
# #         self.history_text.pack(fill=tk.X, pady=5)
# #         self.history_text.config(state=tk.DISABLED)
        
# #         # Clear button
# #         self.clear_btn = tk.Button(history_frame, text="Clear History", 
# #                                   command=self.clear_history,
# #                                   bg="#7f8c8d", fg="white")
# #         self.clear_btn.pack(pady=5)
        
# #         # Display frame elements
# #         self.canvas = tk.Canvas(self.display_frame, bg="black", width=640, height=480)
# #         self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
# #         # Reference section
# #         reference_frame = tk.LabelFrame(self.display_frame, text="Reference", 
# #                                         font=("Arial", 12), bg="#2c3e50", fg="white")
# #         reference_frame.pack(fill=tk.X, pady=10)
        
# #         # Reference grid (will be populated with character references)
# #         self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=100)
# #         self.reference_canvas.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
# #         # Status bar
# #         self.status_var = tk.StringVar(value="Status: Ready")
# #         self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
# #                                   font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
# #                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
# #         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
# #     def enhance_results_frame(self):
# #         """ENHANCED results frame with LARGER Tamil character display"""
# #         # Results section with improved visibility - MADE LARGER AND MORE PROMINENT
# #         self.results_frame = tk.LabelFrame(self.control_frame, text="Detection Results", 
# #                                           font=("Arial", 16, "bold"), bg="#34495e", fg="#f39c12", 
# #                                           padx=15, pady=15, relief=tk.RAISED, bd=3)
# #         self.results_frame.pack(fill=tk.X, pady=15)
        
# #         # Create a frame with a distinct background for the Tamil character - MADE LARGER
# #         char_display_frame = tk.Frame(self.results_frame, bg="#1c2e3c", 
# #                                      padx=15, pady=15, relief=tk.RAISED, bd=3)
# #         char_display_frame.pack(fill=tk.X, pady=10)
        
# #         # Tamil character display - GREATLY INCREASED SIZE
# #         self.tamil_char_var = tk.StringVar(value="")
# #         self.tamil_char_label = tk.Label(char_display_frame, textvariable=self.tamil_char_var,
# #                                         font=(self.tamil_font, 160), bg="#1c2e3c", fg="#ecf0f1",
# #                                         height=1)  # Set fixed height for consistent display
# #         self.tamil_char_label.pack(pady=5)
        
# #         # Pronunciation with better formatting - MADE LARGER
# #         pronunciation_frame = tk.Frame(self.results_frame, bg="#34495e")
# #         pronunciation_frame.pack(fill=tk.X, pady=8)
        
# #         tk.Label(pronunciation_frame, text="Pronunciation:", 
# #                 font=("Arial", 14, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
# #         self.pronunciation_var = tk.StringVar(value="No detection yet")
# #         self.pronunciation_label = tk.Label(pronunciation_frame, textvariable=self.pronunciation_var, 
# #                                           font=("Arial", 14), bg="#34495e", fg="white")
# #         self.pronunciation_label.pack(side=tk.LEFT, padx=5)
        
# #         # Confidence with progress bar - MADE LARGER
# #         confidence_frame = tk.Frame(self.results_frame, bg="#34495e")
# #         confidence_frame.pack(fill=tk.X, pady=8)
        
# #         tk.Label(confidence_frame, text="Confidence:", 
# #                 font=("Arial", 14, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
# #         self.confidence_var = tk.StringVar(value="0.00%")
# #         self.confidence_label = tk.Label(confidence_frame, textvariable=self.confidence_var, 
# #                                         font=("Arial", 14), bg="#34495e", fg="white")
# #         self.confidence_label.pack(side=tk.LEFT, padx=5)
        
# #         # Add a larger progress bar for confidence
# #         self.confidence_progress_frame = tk.Frame(self.results_frame, bg="#34495e", height=30)
# #         self.confidence_progress_frame.pack(fill=tk.X, pady=8)
        
# #         self.confidence_progress = tk.Canvas(self.confidence_progress_frame, 
# #                                             bg="#2c3e50", height=30, bd=0, highlightthickness=0)
# #         self.confidence_progress.pack(fill=tk.X)
    
# #     def update_threshold_label(self, event=None):
# #         """Update the threshold value label"""
# #         self.threshold_value_label.config(text=f"{self.confidence_threshold.get():.1f}")
        
# #     def browse_model(self):
# #         file_path = filedialog.askopenfilename(filetypes=[
# #             ("Keras Model", "*.keras"), 
# #             ("H5 Model", "*.h5"),
# #             ("All Files", "*.*")
# #         ])
# #         if file_path:
# #             self.model_path_var.set(file_path)
            
# #     def browse_labels(self):
# #         file_path = filedialog.askopenfilename(filetypes=[
# #             ("JSON Files", "*.json"),
# #             ("All Files", "*.*")
# #         ])
# #         if file_path:
# #             self.labels_path_var.set(file_path)
            
# #     def load_model_and_labels(self):
# #         model_path = self.model_path_var.get()
# #         labels_path = self.labels_path_var.get()
        
# #         if not model_path:
# #             messagebox.showerror("Error", "Please select a model file")
# #             return
            
# #         if not labels_path:
# #             messagebox.showerror("Error", "Please select a labels file")
# #             return
            
# #         if not os.path.exists(model_path):
# #             messagebox.showerror("Error", f"Model file not found: {model_path}")
# #             return
            
# #         if not os.path.exists(labels_path):
# #             messagebox.showerror("Error", f"Labels file not found: {labels_path}")
# #             return
            
# #         try:
# #             self.status_var.set("Status: Loading model and labels...")
# #             self.root.update()
            
# #             # Load the model
# #             self.model = load_model(model_path)
            
# #             # Load the Tamil labels
# #             with open(labels_path, 'r', encoding='utf-8') as f:
# #                 self.tamil_labels = json.load(f)
            
# #             # Convert string keys to integers
# #             self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
# #             self.model_loaded = True
            
# #             # Enable buttons
# #             self.image_btn.config(state=tk.NORMAL)
# #             self.webcam_btn.config(state=tk.NORMAL)
            
# #             # Update status
# #             self.status_var.set("Status: Model and labels loaded successfully")
# #             messagebox.showinfo("Success", "Model and labels loaded successfully")
            
# #             # Create reference grid
# #             self.create_reference_grid()
            
# #         except Exception as e:
# #             self.status_var.set(f"Status: Error loading model or labels")
# #             messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
# #     def create_reference_grid(self):
# #         """Create a scrollable grid of reference Tamil characters"""
# #         # Clear existing content
# #         self.reference_canvas.delete("all")
        
# #         # Create a frame inside the canvas to hold the characters
# #         frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
# #         self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
# #         # Add characters in a grid (10 per row)
# #         row, col = 0, 0
# #         self.reference_labels = {}  # Store references to labels for highlighting
        
# #         for char_id in sorted(self.tamil_labels.keys()):
# #             if char_id == 247:  # Skip background class (if applicable)
# #                 continue
                
# #             # Create frame for each character
# #             char_frame = tk.Frame(frame, bg="#34495e", width=60, height=60, 
# #                                  padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
# #             char_frame.grid(row=row, column=col, padx=3, pady=3)
# #             char_frame.grid_propagate(False)  # Keep fixed size
            
# #             # Add Tamil character with improved font
# #             char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
# #                                  font=(self.tamil_font, 16), bg="#34495e", fg="white")
# #             char_label.pack(expand=True)
            
# #             # Store reference to this label
# #             self.reference_labels[self.tamil_labels[char_id]["tamil"]] = char_label
            
# #             # Tooltip with pronunciation
# #             self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
# #             # Update row and column
# #             col += 1
# #             if col >= 10:
# #                 col = 0
# #                 row += 1
        
# #         # Update the canvas scroll region
# #         frame.update_idletasks()
# #         self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
# #         # Add scrollbar
# #         scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
# #                                 command=self.reference_canvas.xview)
# #         self.reference_canvas.config(xscrollcommand=scrollbar.set)
# #         scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
# #     def create_tooltip(self, widget, text):
# #         """Create a tooltip for a widget"""
# #         def enter(event):
# #             # Create a new tooltip window when mouse enters
# #             tooltip = tk.Toplevel(widget)
# #             tooltip.wm_overrideredirect(True)  # Remove window decorations
            
# #             # Create label inside the tooltip window
# #             label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
# #             label.pack()
            
# #             # Position the tooltip near the widget
# #             x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
# #             x += widget.winfo_rootx() + 25
# #             y += widget.winfo_rooty() + 25
# #             tooltip.wm_geometry(f"+{x}+{y}")
            
# #             # Store the tooltip reference on the widget
# #             widget.tooltip = tooltip
            
# #         def leave(event):
# #             # Destroy the tooltip when mouse leaves
# #             if hasattr(widget, 'tooltip'):
# #                 widget.tooltip.destroy()
# #                 delattr(widget, 'tooltip')
            
# #         # Bind events
# #         widget.bind("<Enter>", enter)
# #         widget.bind("<Leave>", leave)
    
# #     def process_image(self):
# #         if not self.model_loaded:
# #             messagebox.showerror("Error", "Please load the model and labels first")
# #             return
            
# #         file_path = filedialog.askopenfilename(filetypes=[
# #             ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
# #             ("All Files", "*.*")
# #         ])
        
# #         if not file_path:
# #             return
            
# #         try:
# #             # Read image
# #             image = cv2.imread(file_path)
            
# #             if image is None:
# #                 messagebox.showerror("Error", "Failed to read image")
# #                 return
                
# #             # Update status while processing
# #             self.status_var.set(f"Status: Processing image {os.path.basename(file_path)}...")
# #             self.root.update()
            
# #             # Extract keypoints and make prediction
# #             result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
# #             # Save a copy of the processed image for debugging (optional)
# #             debug_path = f"debug_{os.path.basename(file_path)}"
# #             cv2.imwrite(debug_path, result_image)
            
# #             # Update display - make sure image is shown
# #             self.display_image(result_image)
# #             self.update_results(tamil_char, pronunciation, confidence)
# #             self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
# #             # Add to history
# #             self.add_to_history(tamil_char, pronunciation, confidence)
            
# #         except Exception as e:
# #             self.status_var.set("Status: Error processing image")
# #             error_msg = f"Failed to process image: {str(e)}"
# #             print(error_msg)  # Print to console for debugging
# #             messagebox.showerror("Error", error_msg)
                
# #     def toggle_webcam(self):
# #         if not self.model_loaded:
# #             messagebox.showerror("Error", "Please load the model and labels first")
# #             return
            
# #         if self.is_webcam_active:
# #             # Stop webcam
# #             self.stop_thread = True
# #             if self.detection_thread:
# #                 self.detection_thread.join(timeout=1.0)
# #             if self.cap and self.cap.isOpened():
# #                 self.cap.release()
# #             self.is_webcam_active = False
# #             self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
# #             self.capture_btn.config(state=tk.DISABLED)
# #             self.status_var.set("Status: Webcam stopped")
# #         else:
# #             # Start webcam
# #             self.cap = cv2.VideoCapture(0)
# #             if not self.cap.isOpened():
# #                 messagebox.showerror("Error", "Failed to open webcam")
# #                 return
                
# #             self.is_webcam_active = True
# #             self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
# #             self.capture_btn.config(state=tk.NORMAL)
# #             self.status_var.set("Status: Webcam active")
            
# #             # Start detection thread
# #             self.stop_thread = False
# #             self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
# #             self.detection_thread.daemon = True
# #             self.detection_thread.start()
            
# #     def webcam_detection_loop(self):
# #         """Process webcam frames and detect Tamil finger spellings"""
# #         prev_char = None
# #         stability_count = 0
        
# #         while not self.stop_thread and self.cap and self.cap.isOpened():
# #             try:
# #                 ret, frame = self.cap.read()
# #                 if not ret:
# #                     print("Failed to read from webcam")
# #                     break
                    
# #                 # Flip the frame horizontally for a more natural view
# #                 frame = cv2.flip(frame, 1)
                    
# #                 # Extract keypoints and make prediction
# #                 result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
# #                 # Stability check (to reduce flickering)
# #                 if tamil_char == prev_char:
# #                     stability_count += 1
# #                 else:
# #                     stability_count = 0
                    
# #                 # Only update the display if prediction is stable or very confident
# #                 if stability_count >= 3 or confidence > 80:
# #                     # Use a lambda with no parameters to ensure thread-safety
# #                     self.root.after(0, lambda f=result_frame: self.display_image(f))
# #                     self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
# #                                     self.update_results(t, p, c))
                    
# #                     # If prediction changes with high confidence, add to history
# #                     if tamil_char != prev_char and tamil_char and confidence > 65:
# #                         self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
# #                                         self.add_to_history(t, p, c))
                        
# #                     prev_char = tamil_char
# #                 else:
# #                     # Just update the display without updating results
# #                     self.root.after(0, lambda f=result_frame: self.display_image(f))
                
# #                 # Small delay to reduce CPU usage and make UI more responsive
# #                 time.sleep(0.03)  # Approximate 30 FPS
                
# #             except Exception as e:
# #                 print(f"Error in webcam loop: {str(e)}")
# #                 time.sleep(0.1)
            
# #     def capture_frame(self):
# #         if not self.is_webcam_active or not self.cap:
# #             return
            
# #         ret, frame = self.cap.read()
# #         if not ret:
# #             messagebox.showerror("Error", "Failed to capture frame")
# #             return
            
# #         # Flip the frame horizontally for a more natural view
# #         frame = cv2.flip(frame, 1)
        
# #         # Save the captured frame
# #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# #         save_path = f"capture_{timestamp}.jpg"
# #         cv2.imwrite(save_path, frame)
        
# #         # Process the captured frame
# #         result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
# #         # Update results
# #         self.update_results(tamil_char, pronunciation, confidence)
# #         self.add_to_history(tamil_char, pronunciation, confidence)
        
# #         # Display notification
# #         self.status_var.set(f"Status: Captured frame saved as {save_path}")
# #         messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
# #     def analyze_image(self, image):
# #         """Analyze image and return the recognized Tamil character"""
# #         # Extract hand keypoints
# #         keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
        
# #         if not hands_detected:
# #             return annotated_image, "", "No hands detected", 0.0
            
# #         # Predict gesture
# #         predicted_class, confidence = self.predict_gesture(keypoints)
        
# #         # Get Tamil character and pronunciation
# #         if predicted_class in self.tamil_labels:
# #             tamil_char = self.tamil_labels[predicted_class]["tamil"]
# #             pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
# #         else:
# #             tamil_char = "?"
# #             pronunciation = f"Unknown class: {predicted_class}"
        
# #         # Add prediction text to image - MADE LARGER
# #         cv2.putText(annotated_image, pronunciation, (10, 40), 
# #                     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
# #         cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 80), 
# #                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        
# #         return annotated_image, tamil_char, pronunciation, confidence
            
# #     def extract_hand_keypoints(self, image):
# #         """Extract hand keypoints using MediaPipe"""
# #         # Convert to RGB for MediaPipe
# #         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
# #         # Process image with MediaPipe
# #         results = self.hands.process(image_rgb)
        
# #         # Initialize placeholders for hand keypoints
# #         left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
# #         right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
# #         # Make a copy of the image for drawing
# #         annotated_image = image.copy()
        
# #         # Extract keypoints if hands are detected
# #         if results.multi_hand_landmarks:
# #             for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
# #                 hand_keypoints = []
# #                 for landmark in hand_landmarks.landmark:
# #                     hand_keypoints.append(landmark.x)
# #                     hand_keypoints.append(landmark.x)
# #                     hand_keypoints.append(landmark.y)
                
# #                 # Assign to left or right hand (simplified for demonstration)
# #                 if hand_idx == 0:
# #                     left_hand = hand_keypoints
# #                 elif hand_idx == 1:
# #                     right_hand = hand_keypoints
                
# #                 # Draw landmarks on the image - MADE LARGER AND MORE VISIBLE
# #                 self.mp_drawing.draw_landmarks(
# #                     annotated_image,
# #                     hand_landmarks,
# #                     self.mp_hands.HAND_CONNECTIONS,
# #                     self.mp_drawing_styles.get_default_hand_landmarks_style(),
# #                     self.mp_drawing_styles.get_default_hand_connections_style()
# #                 )
        
# #         # Concatenate left & right hand keypoints
# #         data_aux = np.concatenate([left_hand, right_hand])
        
# #         return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
# #     def predict_gesture(self, keypoints):
# #         """Predict the Tamil character gesture"""
# #         # Reshape input for LSTM: (samples=1, time steps=1, features=84)
# #         input_data = keypoints.reshape(1, 1, 84)
        
# #         # Make prediction with the model
# #         prediction = self.model.predict(input_data, verbose=0)
        
# #         # Get the class with highest probability
# #         predicted_class = np.argmax(prediction)
# #         confidence = np.max(prediction) * 100
        
# #         return predicted_class, confidence
            
# #     def display_image(self, image):
# #         """Display image on canvas with proper scaling"""
# #         try:
# #             # Convert OpenCV BGR image to RGB for Tkinter
# #             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
# #             # Get canvas dimensions
# #             canvas_width = self.canvas.winfo_width()
# #             canvas_height = self.canvas.winfo_height()
            
# #             # If canvas hasn't been fully initialized yet, use default values
# #             if canvas_width <= 1 or canvas_height <= 1:
# #                 canvas_width = 640  # Default width
# #                 canvas_height = 480  # Default height
            
# #             # Calculate scaling factor to fit canvas while maintaining aspect ratio
# #             img_height, img_width = image_rgb.shape[:2]
# #             scale = min(canvas_width/img_width, canvas_height/img_height)
            
# #             # New dimensions
# #             new_width = int(img_width * scale)
# #             new_height = int(img_height * scale)
            
# #             # Resize image
# #             if scale != 1.0:  # Only resize if needed
# #                 image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
# #                                       interpolation=cv2.INTER_AREA)
            
# #             # Convert to PhotoImage
# #             image_pil = Image.fromarray(image_rgb)
# #             image_tk = ImageTk.PhotoImage(image=image_pil)
            
# #             # Clear previous content and update canvas
# #             self.canvas.delete("all")
            
# #             # Center the image on the canvas
# #             x_offset = max(0, (canvas_width - new_width) // 2)
# #             y_offset = max(0, (canvas_height - new_height) // 2)
            
# #             # Draw a border around the image area
# #             self.canvas.create_rectangle(
# #                 x_offset-2, y_offset-2, 
# #                 x_offset+new_width+2, y_offset+new_height+2,
# #                 outline="#3498db", width=2
# #             )
            
# #             # Create image
# #             self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
# #             self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
# #             # Force update to ensure image is displayed
# #             self.canvas.update()
            
# #         except Exception as e:
# #             print(f"Error displaying image: {str(e)}")
        
# #     def update_results(self, tamil_char, pronunciation, confidence):
# #         """Update the results display with enhanced visuals"""
# #         self.tamil_char_var.set(tamil_char)
# #         self.pronunciation_var.set(pronunciation)
# #         self.confidence_var.set(f"{confidence:.2f}%")
# #         self.update_confidence_progress(confidence)
        
# #         # Highlight the detected character in the reference grid
# #         self.highlight_reference_character(tamil_char)

# #     def update_confidence_progress(self, confidence):
# #         """Update the confidence progress bar - MADE LARGER AND MORE VISIBLE"""
# #         self.confidence_progress.delete("all")
# #         width = self.confidence_progress.winfo_width()
# #         if width < 10:  # Not yet properly initialized
# #             width = 200
        
# #         # Draw the background
# #         self.confidence_progress.create_rectangle(0, 0, width, 30, fill="#2c3e50", outline="")
        
# #         # Draw the progress bar
# #         progress_width = int(width * confidence / 100)
        
# #         # Color based on confidence level
# #         if confidence < 30:
# #             color = "#e74c3c"  # Red for low confidence
# #         elif confidence < 70:
# #             color = "#f39c12"  # Orange for medium confidence
# #         else:
# #             color = "#2ecc71"  # Green for high confidence
        
# #         self.confidence_progress.create_rectangle(0, 0, progress_width, 30, 
# #                                                  fill=color, outline="")
        
# #         # Add text - LARGER FONT
# #         self.confidence_progress.create_text(width/2, 15, 
# #                                             text=f"{confidence:.2f}%", 
# #                                             fill="white", font=("Arial", 14, "bold"))
    
# #     def highlight_reference_character(self, tamil_char):
# #         """Highlight the detected character in the reference grid"""
# #         # Reset all characters to normal background
# #         for label in self.reference_labels.values():
# #             label.config(bg="#34495e")
        
# #         # Highlight the detected character if it exists in our reference grid
# #         if tamil_char in self.reference_labels:
# #             self.reference_labels[tamil_char].config(bg="#e74c3c")  # Highlight with a red background
        
# #     def add_to_history(self, tamil_char, pronunciation, confidence):
# #         """Add detection to history"""
# #         if not tamil_char:  # Skip empty detections
# #             return
            
# #         timestamp = datetime.now().strftime("%H:%M:%S")
# #         history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
# #         # Enable text widget for editing
# #         self.history_text.config(state=tk.NORMAL)
        
# #         # Insert at the beginning
# #         self.history_text.insert("1.0", history_entry)
        
# #         # Limit history length
# #         if float(self.history_text.index('end-1c').split('.')[0]) > 20:
# #             self.history_text.delete("20.0", tk.END)
            
# #         # Disable editing
# #         self.history_text.config(state=tk.DISABLED)
        
# #     def clear_history(self):
# #         """Clear detection history"""
# #         self.history_text.config(state=tk.NORMAL)
# #         self.history_text.delete("1.0", tk.END)
# #         self.history_text.config(state=tk.DISABLED)
        
# #     def cleanup(self):
# #         """Clean up resources before closing"""
# #         if self.cap and self.cap.isOpened():
# #             self.cap.release()
# #         self.stop_thread = True
# #         if self.detection_thread:
# #             self.detection_thread.join(timeout=1.0)
# #         print("Application closed, resources released")

# # def create_tamil_label_mapping():
# #     """Create the Tamil character label mapping"""
# #     # Check if labels file already exists
# #     if os.path.exists("tamil_labels.json"):
# #         print("Tamil labels file already exists.")
# #         return
    
# #     # If we needed to create a default Tamil labels file,
# #     # we would add that code here. For now, we'll assume
# #     # the file is provided by the user.
# #     print("Tamil labels file not found. Please provide a valid labels file.")

# # def main():
# #     # Ensure label mapping file exists
# #     create_tamil_label_mapping()
    
# #     # Create and run the GUI
# #     root = tk.Tk()
# #     app = TamilFingerSpellingGUI(root)
    
# #     # Set up cleanup on exit
# #     root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
# #     # Start the GUI event loop
# #     root.mainloop()

# # if __name__ == "__main__":
# #     main()



# import os
# import cv2
# import json
# import pickle
# import numpy as np
# import tensorflow as tf
# import mediapipe as mp
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from tkinter import font as tkfont
# from tensorflow.keras.models import load_model
# from PIL import Image, ImageTk, ImageFont, ImageDraw
# import threading
# from datetime import datetime
# import time
# import platform

# class TamilFingerSpellingGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Tamil Finger Spelling Recognition")
#         self.root.geometry("1200x800")
#         self.root.configure(bg="#2c3e50")
        
#         # Variables
#         self.model = None
#         self.model_loaded = False
#         self.cap = None
#         self.is_webcam_active = False
#         self.detection_thread = None
#         self.stop_thread = False
#         self.tamil_labels = None
        
#         # Setup Tamil fonts
#         self.setup_fonts()
        
#         # Default paths
#         self.default_model_path = "best_lstm_model (3).keras"
#         self.default_labels_path = "tamil_labels.json"
        
#         # MediaPipe setup
#         self.mp_hands = mp.solutions.hands
#         self.mp_drawing = mp.solutions.drawing_utils
#         self.mp_drawing_styles = mp.solutions.drawing_styles
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=2,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5
#         )
        
#         # Create UI elements
#         self.create_widgets()
        
#         # Check for default files
#         self.check_default_files()
        
#     def setup_fonts(self):
#         """Setup fonts for Tamil display"""
#         # Check operating system for appropriate Tamil fonts
#         system = platform.system()
        
#         if system == "Windows":
#             tamil_fonts = ["Latha", "Nirmala UI", "Tamil Sangam MN", "Arial Unicode MS"]
#         elif system == "Darwin":  # macOS
#             tamil_fonts = ["Tamil Sangam MN", "InaiMathi", "Arial Unicode MS"]
#         else:  # Linux and others
#             tamil_fonts = ["Noto Sans Tamil", "Lohit Tamil", "FreeSans", "Arial Unicode MS"]
        
#         # Find first available Tamil font
#         available_fonts = list(tkfont.families())
#         self.tamil_font = None
        
#         for font_name in tamil_fonts:
#             if font_name in available_fonts:
#                 self.tamil_font = font_name
#                 print(f"Using Tamil font: {font_name}")
#                 break
        
#         # If no Tamil font found, use a default font and notify user
#         if not self.tamil_font:
#             self.tamil_font = "TkDefaultFont"
#             print("Warning: No Tamil font found. Install a Tamil font for proper display.")
#             messagebox.showwarning("Font Warning", 
#                 "No Tamil font found. Install a Tamil font like 'Noto Sans Tamil' for proper display.")
    
#     def check_default_files(self):
#         """Check if default model and label files exist and load them"""
#         if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
#             self.model_path_var.set(self.default_model_path)
#             self.labels_path_var.set(self.default_labels_path)
#             self.load_model_and_labels()
        
#     def create_widgets(self):
#         # Main frames layout - Using a different approach for better balance
#         self.main_frame = tk.Frame(self.root, bg="#2c3e50")
#         self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Create a 2x2 grid layout
#         self.main_frame.columnconfigure(0, weight=1, minsize=300)  # Control column
#         self.main_frame.columnconfigure(1, weight=3, minsize=600)  # Display column
#         self.main_frame.rowconfigure(0, weight=1)  # Top row
#         self.main_frame.rowconfigure(1, weight=1)  # Bottom row
        
#         # Create four main sections in the grid
#         self.top_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
#         self.top_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
#         self.bottom_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
#         self.bottom_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
        
#         # Place frames in the grid
#         self.top_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
#         self.top_right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
#         self.bottom_left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
#         self.bottom_right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
#         # Title and logo in top left
#         title_frame = tk.Frame(self.top_left_frame, bg="#34495e")
#         title_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(title_frame, text="Tamil Finger Spelling", 
#                 font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=2)
#         tk.Label(title_frame, text="Recognition System", 
#                 font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
#         # *** DETECTION RESULTS in top left (below title) ***
#         self.enhance_results_frame(self.top_left_frame)
        
#         # *** MODEL SETTINGS in bottom left ***
#         # Model and labels loading section
#         files_frame = tk.LabelFrame(self.bottom_left_frame, text="Model & Labels", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         files_frame.pack(fill=tk.X, pady=5)
        
#         # Model path
#         tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
#         self.model_path_var = tk.StringVar()
#         self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
#         self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
#         self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
#                                          bg="#3498db", fg="white", width=6)
#         self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
#         # Labels path
#         tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
#         self.labels_path_var = tk.StringVar()
#         self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
#         self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
#         self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
#                                           bg="#3498db", fg="white", width=6)
#         self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
#         # Load button
#         self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
#                                  command=self.load_model_and_labels,
#                                  bg="#2ecc71", fg="white", width=15, height=2)
#         self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
#         # *** INPUT OPTIONS in bottom left (below model settings) ***
#         # Input options section
#         input_frame = tk.LabelFrame(self.bottom_left_frame, text="Input Options", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         input_frame.pack(fill=tk.X, pady=5)
        
#         button_frame = tk.Frame(input_frame, bg="#34495e")
#         button_frame.pack(fill=tk.X)
        
#         # Create a grid for better button layout
#         button_frame.columnconfigure(0, weight=1)
#         button_frame.columnconfigure(1, weight=1)
        
#         self.image_btn = tk.Button(button_frame, text="Upload Image", command=self.process_image, 
#                                   bg="#e74c3c", fg="white", width=15, height=2, state=tk.DISABLED)
#         self.image_btn.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        
#         self.webcam_btn = tk.Button(button_frame, text="Start Webcam", command=self.toggle_webcam, 
#                                    bg="#9b59b6", fg="white", width=15, height=2, state=tk.DISABLED)
#         self.webcam_btn.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
#         self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
#                                     bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
#         self.capture_btn.pack(pady=5)
        
#         # Detection parameters section
#         params_frame = tk.LabelFrame(self.bottom_left_frame, text="Detection Parameters", 
#                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=5)
#         params_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
#         self.confidence_threshold = tk.DoubleVar(value=0.5)
#         confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
#                                      variable=self.confidence_threshold, 
#                                      orient=tk.HORIZONTAL, length=200)
#         confidence_scale.pack(fill=tk.X, pady=5)
        
#         # Create a label to display the current value
#         self.threshold_value_label = tk.Label(params_frame, text="0.5", bg="#34495e", fg="white")
#         self.threshold_value_label.pack(anchor=tk.E)
        
#         # Update label when scale changes
#         confidence_scale.bind("<Motion>", self.update_threshold_label)
        
#         # *** CAMERA VIEW in top right ***
#         # Display frame elements - Taking most of the right side
#         camera_frame = tk.LabelFrame(self.top_right_frame, text="Camera View", 
#                                     font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
#         camera_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
#         self.canvas = tk.Canvas(camera_frame, bg="black", width=640, height=480)
#         self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
#         # *** HISTORY and REFERENCE in bottom right ***
#         # Bottom right area split into two sections
#         ref_history_frame = tk.Frame(self.bottom_right_frame, bg="#2c3e50")
#         ref_history_frame.pack(fill=tk.BOTH, expand=True)
        
#         # History section
#         history_frame = tk.LabelFrame(ref_history_frame, text="Detection History", 
#                                      font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         self.history_text = tk.Text(history_frame, width=25, height=10, bg="#2c3e50", fg="white",
#                                    font=("Arial", 10))
#         self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)
#         self.history_text.config(state=tk.DISABLED)
        
#         # Clear button
#         self.clear_btn = tk.Button(history_frame, text="Clear History", 
#                                   command=self.clear_history,
#                                   bg="#7f8c8d", fg="white")
#         self.clear_btn.pack(pady=5)
        
#         # Reference section
#         reference_frame = tk.LabelFrame(ref_history_frame, text="Reference", 
#                                         font=("Arial", 12), bg="#2c3e50", fg="white")
#         reference_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Reference grid (will be populated with character references)
#         self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=150)
#         self.reference_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Status bar
#         self.status_var = tk.StringVar(value="Status: Ready")
#         self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
#                                   font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
#                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
#     def enhance_results_frame(self, parent_frame):
#         """Enhanced results frame with larger Tamil character display"""
#         # Results section with improved visibility
#         self.results_frame = tk.LabelFrame(parent_frame, text="Detection Results", 
#                                           font=("Arial", 16, "bold"), bg="#34495e", fg="#f39c12", 
#                                           padx=15, pady=10, relief=tk.RAISED, bd=3)
#         self.results_frame.pack(fill=tk.X, pady=5)
        
#         # Create a frame with a distinct background for the Tamil character
#         char_display_frame = tk.Frame(self.results_frame, bg="#1c2e3c", 
#                                      padx=15, pady=10, relief=tk.RAISED, bd=3)
#         char_display_frame.pack(fill=tk.X, pady=5)
        
#         # Tamil character display - Large but not too large
#         self.tamil_char_var = tk.StringVar(value="")
#         self.tamil_char_label = tk.Label(char_display_frame, textvariable=self.tamil_char_var,
#                                         font=(self.tamil_font, 120), bg="#1c2e3c", fg="#ecf0f1",
#                                         height=1)
#         self.tamil_char_label.pack(pady=5)
        
#         # Pronunciation with better formatting
#         pronunciation_frame = tk.Frame(self.results_frame, bg="#34495e")
#         pronunciation_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(pronunciation_frame, text="Pronunciation:", 
#                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
#         self.pronunciation_var = tk.StringVar(value="No detection yet")
#         self.pronunciation_label = tk.Label(pronunciation_frame, textvariable=self.pronunciation_var, 
#                                           font=("Arial", 12), bg="#34495e", fg="white")
#         self.pronunciation_label.pack(side=tk.LEFT, padx=5)
        
#         # Confidence with progress bar
#         confidence_frame = tk.Frame(self.results_frame, bg="#34495e")
#         confidence_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(confidence_frame, text="Confidence:", 
#                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
#         self.confidence_var = tk.StringVar(value="0.00%")
#         self.confidence_label = tk.Label(confidence_frame, textvariable=self.confidence_var, 
#                                         font=("Arial", 12), bg="#34495e", fg="white")
#         self.confidence_label.pack(side=tk.LEFT, padx=5)
        
#         # Add a progress bar for confidence
#         self.confidence_progress_frame = tk.Frame(self.results_frame, bg="#34495e", height=25)
#         self.confidence_progress_frame.pack(fill=tk.X, pady=5)
        
#         self.confidence_progress = tk.Canvas(self.confidence_progress_frame, 
#                                             bg="#2c3e50", height=25, bd=0, highlightthickness=0)
#         self.confidence_progress.pack(fill=tk.X)
    
#     def update_threshold_label(self, event=None):
#         """Update the threshold value label"""
#         self.threshold_value_label.config(text=f"{self.confidence_threshold.get():.1f}")
        
#     def browse_model(self):
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("Keras Model", "*.keras"), 
#             ("H5 Model", "*.h5"),
#             ("All Files", "*.*")
#         ])
#         if file_path:
#             self.model_path_var.set(file_path)
            
#     def browse_labels(self):
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("JSON Files", "*.json"),
#             ("All Files", "*.*")
#         ])
#         if file_path:
#             self.labels_path_var.set(file_path)
            
#     def load_model_and_labels(self):
#         model_path = self.model_path_var.get()
#         labels_path = self.labels_path_var.get()
        
#         if not model_path:
#             messagebox.showerror("Error", "Please select a model file")
#             return
            
#         if not labels_path:
#             messagebox.showerror("Error", "Please select a labels file")
#             return
            
#         if not os.path.exists(model_path):
#             messagebox.showerror("Error", f"Model file not found: {model_path}")
#             return
            
#         if not os.path.exists(labels_path):
#             messagebox.showerror("Error", f"Labels file not found: {labels_path}")
#             return
            
#         try:
#             self.status_var.set("Status: Loading model and labels...")
#             self.root.update()
            
#             # Load the model
#             self.model = load_model(model_path)
            
#             # Load the Tamil labels
#             with open(labels_path, 'r', encoding='utf-8') as f:
#                 self.tamil_labels = json.load(f)
            
#             # Convert string keys to integers
#             self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
#             self.model_loaded = True
            
#             # Enable buttons
#             self.image_btn.config(state=tk.NORMAL)
#             self.webcam_btn.config(state=tk.NORMAL)
            
#             # Update status
#             self.status_var.set("Status: Model and labels loaded successfully")
#             messagebox.showinfo("Success", "Model and labels loaded successfully")
            
#             # Create reference grid
#             self.create_reference_grid()
            
#         except Exception as e:
#             self.status_var.set(f"Status: Error loading model or labels")
#             messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
#     def create_reference_grid(self):
#         """Create a scrollable grid of reference Tamil characters"""
#         # Clear existing content
#         self.reference_canvas.delete("all")
        
#         # Create a frame inside the canvas to hold the characters
#         frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
#         self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
#         # Add characters in a grid (10 per row)
#         row, col = 0, 0
#         self.reference_labels = {}  # Store references to labels for highlighting
        
#         for char_id in sorted(self.tamil_labels.keys()):
#             if char_id == 247:  # Skip background class (if applicable)
#                 continue
                
#             # Create frame for each character
#             char_frame = tk.Frame(frame, bg="#34495e", width=60, height=60, 
#                                  padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
#             char_frame.grid(row=row, column=col, padx=3, pady=3)
#             char_frame.grid_propagate(False)  # Keep fixed size
            
#             # Add Tamil character with improved font
#             char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
#                                  font=(self.tamil_font, 16), bg="#34495e", fg="white")
#             char_label.pack(expand=True)
            
#             # Store reference to this label
#             self.reference_labels[self.tamil_labels[char_id]["tamil"]] = char_label
            
#             # Tooltip with pronunciation
#             self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
#             # Update row and column
#             col += 1
#             if col >= 8:  # Reduce columns to fit better
#                 col = 0
#                 row += 1
        
#         # Update the canvas scroll region
#         frame.update_idletasks()
#         self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
#         # Add scrollbar
#         scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
#                                 command=self.reference_canvas.xview)
#         self.reference_canvas.config(xscrollcommand=scrollbar.set)
#         scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
#     def create_tooltip(self, widget, text):
#         """Create a tooltip for a widget"""
#         def enter(event):
#             # Create a new tooltip window when mouse enters
#             tooltip = tk.Toplevel(widget)
#             tooltip.wm_overrideredirect(True)  # Remove window decorations
            
#             # Create label inside the tooltip window
#             label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
#             label.pack()
            
#             # Position the tooltip near the widget
#             x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
#             x += widget.winfo_rootx() + 25
#             y += widget.winfo_rooty() + 25
#             tooltip.wm_geometry(f"+{x}+{y}")
            
#             # Store the tooltip reference on the widget
#             widget.tooltip = tooltip
            
#         def leave(event):
#             # Destroy the tooltip when mouse leaves
#             if hasattr(widget, 'tooltip'):
#                 widget.tooltip.destroy()
#                 delattr(widget, 'tooltip')
            
#         # Bind events
#         widget.bind("<Enter>", enter)
#         widget.bind("<Leave>", leave)
    
#     def process_image(self):
#         if not self.model_loaded:
#             messagebox.showerror("Error", "Please load the model and labels first")
#             return
            
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
#             ("All Files", "*.*")
#         ])
        
#         if not file_path:
#             return
            
#         try:
#             # Read image
#             image = cv2.imread(file_path)
            
#             if image is None:
#                 messagebox.showerror("Error", "Failed to read image")
#                 return
                
#             # Update status while processing
#             self.status_var.set(f"Status: Processing image {os.path.basename(file_path)}...")
#             self.root.update()
            
#             # Extract keypoints and make prediction
#             result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
#             # Save a copy of the processed image for debugging (optional)
#             debug_path = f"debug_{os.path.basename(file_path)}"
#             cv2.imwrite(debug_path, result_image)
            
#             # Update display - make sure image is shown
#             self.display_image(result_image)
#             self.update_results(tamil_char, pronunciation, confidence)
#             self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
#             # Add to history
#             self.add_to_history(tamil_char, pronunciation, confidence)
            
#         except Exception as e:
#             self.status_var.set("Status: Error processing image")
#             error_msg = f"Failed to process image: {str(e)}"
#             print(error_msg)  # Print to console for debugging
#             messagebox.showerror("Error", error_msg)
                
#     def toggle_webcam(self):
#         if not self.model_loaded:
#             messagebox.showerror("Error", "Please load the model and labels first")
#             return
            
#         if self.is_webcam_active:
#             # Stop webcam
#             self.stop_thread = True
#             if self.detection_thread:
#                 self.detection_thread.join(timeout=1.0)
#             if self.cap and self.cap.isOpened():
#                 self.cap.release()
#             self.is_webcam_active = False
#             self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
#             self.capture_btn.config(state=tk.DISABLED)
#             self.status_var.set("Status: Webcam stopped")
#         else:
#             # Start webcam
#             self.cap = cv2.VideoCapture(0)
#             if not self.cap.isOpened():
#                 messagebox.showerror("Error", "Failed to open webcam")
#                 return
                
#             self.is_webcam_active = True
#             self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
#             self.capture_btn.config(state=tk.NORMAL)
#             self.status_var.set("Status: Webcam active")
            
#             # Start detection thread
#             self.stop_thread = False
#             self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
#             self.detection_thread.daemon = True
#             self.detection_thread.start()
            
#     def webcam_detection_loop(self):
#         """Process webcam frames and detect Tamil finger spellings"""
#         prev_char = None
#         stability_count = 0
        
#         while not self.stop_thread and self.cap and self.cap.isOpened():
#             try:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     print("Failed to read from webcam")
#                     break
                    
#                 # Flip the frame horizontally for a more natural view
#                 frame = cv2.flip(frame, 1)
                    
#                 # Extract keypoints and make prediction
#                 result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
#                 # Stability check (to reduce flickering)
#                 if tamil_char == prev_char:
#                     stability_count += 1
#                 else:
#                     stability_count = 0
                    
#                 # Only update the display if prediction is stable or very confident
#                 if stability_count >= 3 or confidence > 80:
#                     # Use a lambda with no parameters to ensure thread-safety
#                     self.root.after(0, lambda f=result_frame: self.display_image(f))
#                     self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
#                                     self.update_results(t, p, c))
                    
#                     # If prediction changes with high confidence, add to history
#                     if tamil_char != prev_char and tamil_char and confidence > 65:
#                         self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
#                                         self.add_to_history(t, p, c))
                        
#                     prev_char = tamil_char
#                 else:
#                     # Just update the display without updating results
#                     self.root.after(0, lambda f=result_frame: self.display_image(f))
                
#                 # Small delay to reduce CPU usage and make UI more responsive
#                 time.sleep(0.03)  # Approximate 30 FPS
                
#             except Exception as e:
#                 print(f"Error in webcam loop: {str(e)}")
#                 time.sleep(0.1)
            
#     def capture_frame(self):
#         if not self.is_webcam_active or not self.cap:
#             return
            
#         ret, frame = self.cap.read()
#         if not ret:
#             messagebox.showerror("Error", "Failed to capture frame")
#             return
            
#         # Flip the frame horizontally for a more natural view
#         frame = cv2.flip(frame, 1)
        
#         # Save the captured frame
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         save_path = f"capture_{timestamp}.jpg"
#         cv2.imwrite(save_path, frame)
        
#         # Process the captured frame
#         result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
#         # Update results
#         self.update_results(tamil_char, pronunciation, confidence)
#         self.add_to_history(tamil_char, pronunciation, confidence)
        
#         # Display notification
#         self.status_var.set(f"Status: Captured frame saved as {save_path}")
#         messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
#     def analyze_image(self, image):
#         """Analyze image and return the recognized Tamil character"""
#         # Extract hand keypoints
#         keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
#         if not hands_detected:
#             return annotated_image, "", "No hands detected", 0.0
            
#         # Predict gesture
#         predicted_class, confidence = self.predict_gesture(keypoints)
        
#         # Get Tamil character and pronunciation
#         if predicted_class in self.tamil_labels:
#             tamil_char = self.tamil_labels[predicted_class]["tamil"]
#             pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
#         else:
#             tamil_char = "?"
#             pronunciation = f"Unknown class: {predicted_class}"
        
#         # Add prediction text to image
#         cv2.putText(annotated_image, pronunciation, (10, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
#         cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 80), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        
#         return annotated_image, tamil_char, pronunciation, confidence
            
#     def extract_hand_keypoints(self, image):
#         """Extract hand keypoints using MediaPipe"""
#         # Convert to RGB for MediaPipe
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
#         # Process image with MediaPipe
#         results = self.hands.process(image_rgb)
        
#         # Initialize placeholders for hand keypoints
#         left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
#         right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
#         # Make a copy of the image for drawing
#         annotated_image = image.copy()
        
#         # Extract keypoints if hands are detected
#         if results.multi_hand_landmarks:
#             for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
#                 hand_keypoints = []
#                 for landmark in hand_landmarks.landmark:
#                     hand_keypoints.append(landmark.x)
#                     hand_keypoints.append(landmark.y)
                
#                 # Assign to left or right hand (simplified for demonstration)
#                 if hand_idx == 0:
#                     left_hand = hand_keypoints
#                 elif hand_idx == 1:
#                     right_hand = hand_keypoints
                
#                 # Draw landmarks on the image
#                 self.mp_drawing.draw_landmarks(
#                     annotated_image,
#                     hand_landmarks,
#                     self.mp_hands.HAND_CONNECTIONS,
#                     self.mp_drawing_styles.get_default_hand_landmarks_style(),
#                     self.mp_drawing_styles.get_default_hand_connections_style()
#                 )
        
#         # Concatenate left & right hand keypoints
#         data_aux = np.concatenate([left_hand, right_hand])
        
#         return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
#     def predict_gesture(self, keypoints):
#         """Predict the Tamil character gesture"""
#         # Reshape input for LSTM: (samples=1, time steps=1, features=84)
#         input_data = keypoints.reshape(1, 1, 84)
        
#         # Make prediction with the model
#         prediction = self.model.predict(input_data, verbose=0)
        
#         # Get the class with highest probability
#         predicted_class = np.argmax(prediction)
#         confidence = np.max(prediction) * 100
        
#         return predicted_class, confidence
            
#     def display_image(self, image):
#         """Display image on canvas with proper scaling"""
#         try:
#             # Convert OpenCV BGR image to RGB for Tkinter
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
#             # Get canvas dimensions
#             canvas_width = self.canvas.winfo_width()
#             canvas_height = self.canvas.winfo_height()
            
#             # If canvas hasn't been fully initialized yet, use default values
#             if canvas_width <= 1 or canvas_height <= 1:
#                 canvas_width = 640  # Default width
#                 canvas_height = 480  # Default height
            
#             # Calculate scaling factor to fit canvas while maintaining aspect ratio
#             img_height, img_width = image_rgb.shape[:2]
#             scale = min(canvas_width/img_width, canvas_height/img_height)
            
#             # New dimensions
#             new_width = int(img_width * scale)
#             new_height = int(img_height * scale)
            
#             # Resize image
#             if scale != 1.0:  # Only resize if needed
#                 image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
#                                       interpolation=cv2.INTER_AREA)
            
#             # Convert to PhotoImage
#             image_pil = Image.fromarray(image_rgb)
#             image_tk = ImageTk.PhotoImage(image=image_pil)
            
#             # Clear previous content and update canvas
#             self.canvas.delete("all")
            
#             # Center the image on the canvas
#             x_offset = max(0, (canvas_width - new_width) // 2)
#             y_offset = max(0, (canvas_height - new_height) // 2)
            
#             # Draw a border around the image area
#             self.canvas.create_rectangle(
#                 x_offset-2, y_offset-2, 
#                 x_offset+new_width+2, y_offset+new_height+2,
#                 outline="#3498db", width=2
#             )
            
#             # Create image
#             self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
#             self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
#             # Force update to ensure image is displayed
#             self.canvas.update()
            
#         except Exception as e:
#             print(f"Error displaying image: {str(e)}")
        
#     def update_results(self, tamil_char, pronunciation, confidence):
#         """Update the results display with enhanced visuals"""
#         self.tamil_char_var.set(tamil_char)
#         self.pronunciation_var.set(pronunciation)
#         self.confidence_var.set(f"{confidence:.2f}%")
#         self.update_confidence_progress(confidence)
        
#         # Highlight the detected character in the reference grid
#         self.highlight_reference_character(tamil_char)

#     def update_confidence_progress(self, confidence):
#         """Update the confidence progress bar"""
#         self.confidence_progress.delete("all")
#         width = self.confidence_progress.winfo_width()
#         if width < 10:  # Not yet properly initialized
#             width = 200
        
#         # Draw the background
#         self.confidence_progress.create_rectangle(0, 0, width, 25, fill="#2c3e50", outline="")
        
#         # Draw the progress bar
#         progress_width = int(width * confidence / 100)
        
#         # Color based on confidence level
#         if confidence < 30:
#             color = "#e74c3c"  # Red for low confidence
#         elif confidence < 70:
#             color = "#f39c12"  # Orange for medium confidence
#         else:
#             color = "#2ecc71"  # Green for high confidence
        
#         self.confidence_progress.create_rectangle(0, 0, progress_width, 25, 
#                                                  fill=color, outline="")
        
#         # Add text
#         self.confidence_progress.create_text(width/2, 13, 
#                                             text=f"{confidence:.2f}%", 
#                                             fill="white", font=("Arial", 12, "bold"))
    
#     def highlight_reference_character(self, tamil_char):
#         """Highlight the detected character in the reference grid"""
#         # Reset all characters to normal background
#         for label in self.reference_labels.values():
#             label.config(bg="#34495e")
        
#         # Highlight the detected character if it exists in our reference grid
#         if tamil_char in self.reference_labels:
#             self.reference_labels[tamil_char].config(bg="#e74c3c")  # Highlight with a red background
        
#     def add_to_history(self, tamil_char, pronunciation, confidence):
#         """Add detection to history"""
#         if not tamil_char:  # Skip empty detections
#             return
            
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
#         # Enable text widget for editing
#         self.history_text.config(state=tk.NORMAL)
        
#         # Insert at the beginning
#         self.history_text.insert("1.0", history_entry)
        
#         # Limit history length
#         if float(self.history_text.index('end-1c').split('.')[0]) > 20:
#             self.history_text.delete("20.0", tk.END)
            
#         # Disable editing
#         self.history_text.config(state=tk.DISABLED)
        
#     def clear_history(self):
#         """Clear detection history"""
#         self.history_text.config(state=tk.NORMAL)
#         self.history_text.delete("1.0", tk.END)
#         self.history_text.config(state=tk.DISABLED)
        
#     def cleanup(self):
#         """Clean up resources before closing"""
#         if self.cap and self.cap.isOpened():
#             self.cap.release()
#         self.stop_thread = True
#         if self.detection_thread:
#             self.detection_thread.join(timeout=1.0)
#         print("Application closed, resources released")

# def create_tamil_label_mapping():
#     """Create the Tamil character label mapping"""
#     # Check if labels file already exists
#     if os.path.exists("tamil_labels.json"):
#         print("Tamil labels file already exists.")
#         return
    
#     # If we needed to create a default Tamil labels file,
#     # we would add that code here. For now, we'll assume
#     # the file is provided by the user.
#     print("Tamil labels file not found. Please provide a valid labels file.")

# def main():
#     # Ensure label mapping file exists
#     create_tamil_label_mapping()
    
#     # Create and run the GUI
#     root = tk.Tk()
#     app = TamilFingerSpellingGUI(root)
    
#     # Set up cleanup on exit
#     root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
#     # Start the GUI event loop
#     root.mainloop()

# if __name__ == "__main__":
#     main()

# import os
# import cv2
# import json
# import pickle
# import numpy as np
# import tensorflow as tf
# import mediapipe as mp
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from tkinter import font as tkfont
# from tensorflow.keras.models import load_model
# from PIL import Image, ImageTk, ImageFont, ImageDraw
# import threading
# from datetime import datetime
# import time
# import platform
# from gtts import gTTS
# import pygame
# import tempfile
# import shutil

# class TamilFingerSpellingGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Tamil Finger Spelling Recognition")
#         self.root.geometry("1200x800")
#         self.root.configure(bg="#2c3e50")
        
#         # Variables
#         self.model = None
#         self.model_loaded = False
#         self.cap = None
#         self.is_webcam_active = False
#         self.detection_thread = None
#         self.stop_thread = False
#         self.tamil_labels = None
        
#         # Word recognition variables
#         self.current_word = ""
#         self.word_capture_active = False
#         self.last_detected_char = ""
#         self.char_stabilization_count = 0
#         self.char_stability_threshold = 10  # Frames of stability before accepting a character
#         self.pygame_initialized = False
        
#         # Setup Tamil fonts
#         self.setup_fonts()
        
#         # Default paths
#         self.default_model_path = "best_lstm_model (3).keras"
#         self.default_labels_path = "tamil_labels.json"
        
#         # MediaPipe setup
#         self.mp_hands = mp.solutions.hands
#         self.mp_drawing = mp.solutions.drawing_utils
#         self.mp_drawing_styles = mp.solutions.drawing_styles
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=2,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5
#         )
        
#         # Create UI elements
#         self.create_widgets()
        
#         # Check for default files
#         self.check_default_files()
        
#     def setup_fonts(self):
#         """Setup fonts for Tamil display"""
#         # Check operating system for appropriate Tamil fonts
#         system = platform.system()
        
#         if system == "Windows":
#             tamil_fonts = ["Latha", "Nirmala UI", "Tamil Sangam MN", "Arial Unicode MS"]
#         elif system == "Darwin":  # macOS
#             tamil_fonts = ["Tamil Sangam MN", "InaiMathi", "Arial Unicode MS"]
#         else:  # Linux and others
#             tamil_fonts = ["Noto Sans Tamil", "Lohit Tamil", "FreeSans", "Arial Unicode MS"]
        
#         # Find first available Tamil font
#         available_fonts = list(tkfont.families())
#         self.tamil_font = None
        
#         for font_name in tamil_fonts:
#             if font_name in available_fonts:
#                 self.tamil_font = font_name
#                 print(f"Using Tamil font: {font_name}")
#                 break
        
#         # If no Tamil font found, use a default font and notify user
#         if not self.tamil_font:
#             self.tamil_font = "TkDefaultFont"
#             print("Warning: No Tamil font found. Install a Tamil font for proper display.")
#             messagebox.showwarning("Font Warning", 
#                 "No Tamil font found. Install a Tamil font like 'Noto Sans Tamil' for proper display.")
    
#     def check_default_files(self):
#         """Check if default model and label files exist and load them"""
#         if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
#             self.model_path_var.set(self.default_model_path)
#             self.labels_path_var.set(self.default_labels_path)
#             self.load_model_and_labels()
        
#     def create_widgets(self):
#         # Main frames layout - Using a different approach for better balance
#         self.main_frame = tk.Frame(self.root, bg="#2c3e50")
#         self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Create a 2x2 grid layout
#         self.main_frame.columnconfigure(0, weight=1, minsize=300)  # Control column
#         self.main_frame.columnconfigure(1, weight=3, minsize=600)  # Display column
#         self.main_frame.rowconfigure(0, weight=1)  # Top row
#         self.main_frame.rowconfigure(1, weight=1)  # Bottom row
        
#         # Create four main sections in the grid
#         self.top_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
#         self.top_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
#         self.bottom_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
#         self.bottom_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
        
#         # Place frames in the grid
#         self.top_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
#         self.top_right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
#         self.bottom_left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
#         self.bottom_right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
#         # Title and logo in top left
#         title_frame = tk.Frame(self.top_left_frame, bg="#34495e")
#         title_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(title_frame, text="Tamil Finger Spelling", 
#                 font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=2)
#         tk.Label(title_frame, text="Recognition System", 
#                 font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
#         # *** DETECTION RESULTS in top left (below title) ***
#         self.enhance_results_frame(self.top_left_frame)
        
#         # *** MODEL SETTINGS in bottom left ***
#         # Model and labels loading section
#         files_frame = tk.LabelFrame(self.bottom_left_frame, text="Model & Labels", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         files_frame.pack(fill=tk.X, pady=5)
        
#         # Model path
#         tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
#         self.model_path_var = tk.StringVar()
#         self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
#         self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
#         self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
#                                          bg="#3498db", fg="white", width=6)
#         self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
#         # Labels path
#         tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
#         self.labels_path_var = tk.StringVar()
#         self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
#         self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
#         self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
#                                           bg="#3498db", fg="white", width=6)
#         self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
#         # Load button
#         self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
#                                  command=self.load_model_and_labels,
#                                  bg="#2ecc71", fg="white", width=15, height=2)
#         self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
#         # *** INPUT OPTIONS in bottom left (below model settings) ***
#         # Input options section
#         input_frame = tk.LabelFrame(self.bottom_left_frame, text="Input Options", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         input_frame.pack(fill=tk.X, pady=5)
        
#         button_frame = tk.Frame(input_frame, bg="#34495e")
#         button_frame.pack(fill=tk.X)
        
#         # Create a grid for better button layout
#         button_frame.columnconfigure(0, weight=1)
#         button_frame.columnconfigure(1, weight=1)
        
#         self.image_btn = tk.Button(button_frame, text="Upload Image", command=self.process_image, 
#                                   bg="#e74c3c", fg="white", width=15, height=2, state=tk.DISABLED)
#         self.image_btn.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        
#         self.webcam_btn = tk.Button(button_frame, text="Start Webcam", command=self.toggle_webcam, 
#                                    bg="#9b59b6", fg="white", width=15, height=2, state=tk.DISABLED)
#         self.webcam_btn.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
#         self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
#                                     bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
#         self.capture_btn.pack(pady=5)
        
#         # Word recognition controls in bottom left (below input options)
#         self.add_word_recognition_controls()
        
#         # Detection parameters section
#         params_frame = tk.LabelFrame(self.bottom_left_frame, text="Detection Parameters", 
#                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=5)
#         params_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
#         self.confidence_threshold = tk.DoubleVar(value=0.5)
#         confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
#                                      variable=self.confidence_threshold, 
#                                      orient=tk.HORIZONTAL, length=200)
#         confidence_scale.pack(fill=tk.X, pady=5)
        
#         # Create a label to display the current value
#         self.threshold_value_label = tk.Label(params_frame, text="0.5", bg="#34495e", fg="white")
#         self.threshold_value_label.pack(anchor=tk.E)
        
#         # Update label when scale changes
#         confidence_scale.bind("<Motion>", self.update_threshold_label)
        
#         # *** CAMERA VIEW in top right ***
#         # Display frame elements - Taking most of the right side
#         camera_frame = tk.LabelFrame(self.top_right_frame, text="Camera View", 
#                                     font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
#         camera_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
#         self.canvas = tk.Canvas(camera_frame, bg="black", width=640, height=480)
#         self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
#         # *** HISTORY and REFERENCE in bottom right ***
#         # Bottom right area split into two sections
#         ref_history_frame = tk.Frame(self.bottom_right_frame, bg="#2c3e50")
#         ref_history_frame.pack(fill=tk.BOTH, expand=True)
        
#         # History section
#         history_frame = tk.LabelFrame(ref_history_frame, text="Detection History", 
#                                      font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         self.history_text = tk.Text(history_frame, width=25, height=10, bg="#2c3e50", fg="white",
#                                    font=("Arial", 10))
#         self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)
#         self.history_text.config(state=tk.DISABLED)
        
#         # Clear button
#         self.clear_btn = tk.Button(history_frame, text="Clear History", 
#                                   command=self.clear_history,
#                                   bg="#7f8c8d", fg="white")
#         self.clear_btn.pack(pady=5)
        
#         # Reference section
#         reference_frame = tk.LabelFrame(ref_history_frame, text="Reference", 
#                                         font=("Arial", 12), bg="#2c3e50", fg="white")
#         reference_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Reference grid (will be populated with character references)
#         self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=150)
#         self.reference_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Status bar
#         self.status_var = tk.StringVar(value="Status: Ready")
#         self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
#                                   font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
#                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
#     def add_word_recognition_controls(self):
#         """Add controls for word recognition"""
#         word_frame = tk.LabelFrame(self.bottom_left_frame, text="Word Recognition", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         word_frame.pack(fill=tk.X, pady=5)
        
#         # Current word display
#         word_display_frame = tk.Frame(word_frame, bg="#2c3e50", padx=10, pady=10)
#         word_display_frame.pack(fill=tk.X, pady=5)
        
#         self.word_var = tk.StringVar(value="")
#         self.word_label = tk.Label(word_display_frame, textvariable=self.word_var,
#                                   font=(self.tamil_font, 24), bg="#2c3e50", fg="white", 
#                                   wraplength=250, justify=tk.LEFT)
#         self.word_label.pack(fill=tk.X, pady=5)
        
#         # Word capture controls
#         button_frame = tk.Frame(word_frame, bg="#34495e")
#         button_frame.pack(fill=tk.X, pady=5)
        
#         # Add character button
#         self.add_char_btn = tk.Button(button_frame, text="Add Character", 
#                                      command=self.add_current_char_to_word,
#                                      bg="#3498db", fg="white", state=tk.DISABLED)
#         self.add_char_btn.grid(row=0, column=0, padx=5, pady=5)
        
#         # Start/Stop word capture
#         self.word_toggle_btn = tk.Button(button_frame, text="Start Word Capture", 
#                                         command=self.toggle_word_capture,
#                                         bg="#2ecc71", fg="white", state=tk.DISABLED)
#         self.word_toggle_btn.grid(row=0, column=1, padx=5, pady=5)
        
#         # Add a row of buttons for word actions
#         actions_frame = tk.Frame(word_frame, bg="#34495e")
#         actions_frame.pack(fill=tk.X, pady=5)
        
#         # Speak button
#         self.speak_btn = tk.Button(actions_frame, text="Speak Word", 
#                                   command=self.speak_current_word,
#                                   bg="#9b59b6", fg="white", state=tk.DISABLED)
#         self.speak_btn.grid(row=0, column=0, padx=5, pady=5)
        
#         # Clear button
#         self.clear_word_btn = tk.Button(actions_frame, text="Clear Word", 
#                                        command=self.clear_current_word,
#                                        bg="#e74c3c", fg="white", state=tk.DISABLED)
#         self.clear_word_btn.grid(row=0, column=1, padx=5, pady=5)
        
#         # Save button
#         self.save_word_btn = tk.Button(actions_frame, text="Save Word", 
#                                       command=self.save_current_word,
#                                       bg="#f39c12", fg="white", state=tk.DISABLED)
#         self.save_word_btn.grid(row=0, column=2, padx=5, pady=5)
    
#     def toggle_word_capture(self):
#         """Toggle word capture mode"""
#         if not self.word_capture_active:
#             self.word_capture_active = True
#             self.word_toggle_btn.config(text="Stop Word Capture", bg="#e74c3c")
#             self.add_char_btn.config(state=tk.NORMAL)
#             self.clear_word_btn.config(state=tk.NORMAL)
#             self.status_var.set("Status: Word capture active - make gestures to spell a word")
#         else:
#             self.word_capture_active = False
#             self.word_toggle_btn.config(text="Start Word Capture", bg="#2ecc71")
#             self.status_var.set("Status: Word capture stopped")
    
#     def add_current_char_to_word(self):
#         """Add the currently detected character to the word"""
#         if not self.tamil_char_var.get():
#             messagebox.showinfo("Info", "No character currently detected")
#             return
            
#         # Add the character to the current word
#         self.current_word += self.tamil_char_var.get()
#         self.word_var.set(self.current_word)
        
#         # Enable buttons for word actions
#         self.speak_btn.config(state=tk.NORMAL)
#         self.save_word_btn.config(state=tk.NORMAL)
#         self.clear_word_btn.config(state=tk.NORMAL)
        
#         # Provide feedback
#         self.status_var.set(f"Status: Added '{self.tamil_char_var.get()}' to word")
    
#     def clear_current_word(self):
#         """Clear the current word"""
#         self.current_word = ""
#         self.word_var.set("")
#         self.speak_btn.config(state=tk.DISABLED)
#         self.save_word_btn.config(state=tk.DISABLED)
#         self.status_var.set("Status: Word cleared")
    
#     def save_current_word(self):
#         """Save the current word to a file"""
#         if not self.current_word:
#             messagebox.showinfo("Info", "No word to save")
#             return
            
#         # Get current timestamp for filename
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"word_{timestamp}.txt"
        
#         # Save the word with metadata
#         try:
#             with open(filename, 'w', encoding='utf-8') as f:
#                 f.write(f"Word: {self.current_word}\n")
#                 f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
#                 # Add to history
#                 self.add_to_history(self.current_word, "Word saved", 100.0)
                
#             self.status_var.set(f"Status: Word saved as {filename}")
#             messagebox.showinfo("Success", f"Word saved as {filename}")
#         except Exception as e:
#             self.status_var.set("Status: Error saving word")
#             messagebox.showerror("Error", f"Failed to save word: {str(e)}")
    
#     def speak_current_word(self):
#         """Speak the current Tamil word using gTTS"""
#         if not self.current_word:
#             messagebox.showinfo("Info", "No word to speak")
#             return
            
#         try:
#             # Initialize pygame mixer if not already done
#             if not self.pygame_initialized:
#                 pygame.mixer.init()
#                 self.pygame_initialized = True
            
#             # Create a temporary file
#             temp_dir = tempfile.mkdtemp()
#             temp_file = os.path.join(temp_dir, "temp.mp3")
            
#             # Generate speech
#             self.status_var.set("Status: Generating speech...")
#             self.root.update()
            
#             tts = gTTS(text=self.current_word, lang='ta', slow=False)
#             tts.save(temp_file)
            
#             # Play the speech
#             pygame.mixer.music.load(temp_file)
#             pygame.mixer.music.play()
            
#             # Wait for playback to finish
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
            
#             # Clean up temporary files
#             shutil.rmtree(temp_dir)
            
#             self.status_var.set("Status: Word spoken")
#         except Exception as e:
#             self.status_var.set("Status: Error speaking word")
#             messagebox.showerror("Error", f"Failed to speak word: {str(e)}")
    
#     def enhance_results_frame(self, parent_frame):
#         """Enhanced results frame with larger Tamil character display"""
#         # Results section with improved visibility
#         self.results_frame = tk.LabelFrame(parent_frame, text="Detection Results", 
#                                           font=("Arial", 16, "bold"), bg="#34495e", fg="#f39c12", 
#                                           padx=15, pady=10, relief=tk.RAISED, bd=3)
#         self.results_frame.pack(fill=tk.X, pady=5)
        
#         # Create a frame with a distinct background for the Tamil character
#         char_display_frame = tk.Frame(self.results_frame, bg="#1c2e3c", 
#                                      padx=15, pady=10, relief=tk.RAISED, bd=3)
#         char_display_frame.pack(fill=tk.X, pady=5)
        
#         # Tamil character display - Large but not too large
#         self.tamil_char_var = tk.StringVar(value="")
#         self.tamil_char_label = tk.Label(char_display_frame, textvariable=self.tamil_char_var,
#                                         font=(self.tamil_font, 120), bg="#1c2e3c", fg="#ecf0f1",
#                                         height=1)
#         self.tamil_char_label.pack(pady=5)
        
#         # Pronunciation with better formatting
#         pronunciation_frame = tk.Frame(self.results_frame, bg="#34495e")
#         pronunciation_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(pronunciation_frame, text="Pronunciation:", 
#                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
#         self.pronunciation_var = tk.StringVar(value="No detection yet")
#         self.pronunciation_label = tk.Label(pronunciation_frame, textvariable=self.pronunciation_var, 
#                                           font=("Arial", 12), bg="#34495e", fg="white")
#         self.pronunciation_label.pack(side=tk.LEFT, padx=5)
        
#         # Confidence with progress bar
#         confidence_frame = tk.Frame(self.results_frame, bg="#34495e")
#         confidence_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(confidence_frame, text="Confidence:", 
#                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
#         self.confidence_var = tk.StringVar(value="0.00%")
#         self.confidence_label = tk.Label(confidence_frame, textvariable=self.confidence_var, 
#                                         font=("Arial", 12), bg="#34495e", fg="white")
#         self.confidence_label.pack(side=tk.LEFT, padx=5)
        
#         # Add a progress bar for confidence
#         self.confidence_progress_frame = tk.Frame(self.results_frame, bg="#34495e", height=25)
#         self.confidence_progress_frame.pack(fill=tk.X, pady=5)
        
#         self.confidence_progress = tk.Canvas(self.confidence_progress_frame, 
#                                             bg="#2c3e50", height=25, bd=0, highlightthickness=0)
#         self.confidence_progress.pack(fill=tk.X)
    
#     def update_threshold_label(self, event=None):
#         """Update the threshold value label"""
#         self.threshold_value_label.config(text=f"{self.confidence_threshold.get():.1f}")
        
#     def browse_model(self):
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("Keras Model", "*.keras"), 
#             ("H5 Model", "*.h5"),
#             ("All Files", "*.*")
#         ])
#         if file_path:
#             self.model_path_var.set(file_path)
            
#     def browse_labels(self):
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("JSON Files", "*.json"),
#             ("All Files", "*.*")
#         ])
#         if file_path:
#             self.labels_path_var.set(file_path)
            
#     def load_model_and_labels(self):
#         model_path = self.model_path_var.get()
#         labels_path = self.labels_path_var.get()
        
#         if not model_path:
#             messagebox.showerror("Error", "Please select a model file")
#             return
            
#         if not labels_path:
#             messagebox.showerror("Error", "Please select a labels file")
#             return
            
#         if not os.path.exists(model_path):
#             messagebox.showerror("Error", f"Model file not found: {model_path}")
#             return
            
#         if not os.path.exists(labels_path):
#             messagebox.showerror("Error", f"Labels file not found: {labels_path}")
#             return
            
#         try:
#             self.status_var.set("Status: Loading model and labels...")
#             self.root.update()
            
#             # Load the model
#             self.model = load_model(model_path)
            
#             # Load the Tamil labels
#             with open(labels_path, 'r', encoding='utf-8') as f:
#                 self.tamil_labels = json.load(f)
            
#             # Convert string keys to integers
#             self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
#             self.model_loaded = True
            
#             # Enable buttons
#             self.image_btn.config(state=tk.NORMAL)
#             self.webcam_btn.config(state=tk.NORMAL)
#             self.word_toggle_btn.config(state=tk.NORMAL)
            
#             # Update status
#             self.status_var.set("Status: Model and labels loaded successfully")
#             messagebox.showinfo("Success", "Model and labels loaded successfully")
            
#             # Create reference grid
#             self.create_reference_grid()
            
#         except Exception as e:
#             self.status_var.set(f"Status: Error loading model or labels")
#             messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
#     def create_reference_grid(self):
#         """Create a scrollable grid of reference Tamil characters"""
#         # Clear existing content
#         self.reference_canvas.delete("all")
        
#         # Create a frame inside the canvas to hold the characters
#         frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
#         self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
#         # Add characters in a grid (10 per row)
#         row, col = 0, 0
#         self.reference_labels = {}  # Store references to labels for highlighting
        
#         for char_id in sorted(self.tamil_labels.keys()):
#             if char_id == 247:  # Skip background class (if applicable)
#                 continue
                
#             # Create frame for each character
#             char_frame = tk.Frame(frame, bg="#34495e", width=60, height=60, 
#                                  padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
#             char_frame.grid(row=row, column=col, padx=3, pady=3)
#             char_frame.grid_propagate(False)  # Keep fixed size
            
#             # Add Tamil character with improved font
#             char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
#                                  font=(self.tamil_font, 16), bg="#34495e", fg="white")
#             char_label.pack(expand=True)
            
#             # Store reference to this label
#             self.reference_labels[self.tamil_labels[char_id]["tamil"]] = char_label
            
#             # Tooltip with pronunciation
#             self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
#             # Update row and column
#             col += 1
#             if col >= 8:  # Reduce columns to fit better
#                 col = 0
#                 row += 1
        
#         # Update the canvas scroll region
#         frame.update_idletasks()
#         self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
#         # Add scrollbar
#         scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
#                                 command=self.reference_canvas.xview)
#         self.reference_canvas.config(xscrollcommand=scrollbar.set)
#         scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
#     def create_tooltip(self, widget, text):
#         """Create a tooltip for a widget"""
#         def enter(event):
#             # Create a new tooltip window when mouse enters
#             tooltip = tk.Toplevel(widget)
#             tooltip.wm_overrideredirect(True)  # Remove window decorations
            
#             # Create label inside the tooltip window
#             label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
#             label.pack()
            
#             # Position the tooltip near the widget
#             x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
#             x += widget.winfo_rootx() + 25
#             y += widget.winfo_rooty() + 25
#             tooltip.wm_geometry(f"+{x}+{y}")
            
#             # Store the tooltip reference on the widget
#             widget.tooltip = tooltip
            
#         def leave(event):
#             # Destroy the tooltip when mouse leaves
#             if hasattr(widget, 'tooltip'):
#                 widget.tooltip.destroy()
#                 delattr(widget, 'tooltip')
            
#         # Bind events
#         widget.bind("<Enter>", enter)
#         widget.bind("<Leave>", leave)
    
#     def process_image(self):
#         if not self.model_loaded:
#             messagebox.showerror("Error", "Please load the model and labels first")
#             return
            
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
#             ("All Files", "*.*")
#         ])
        
#         if not file_path:
#             return
            
#         try:
#             # Read image
#             image = cv2.imread(file_path)
            
#             if image is None:
#                 messagebox.showerror("Error", "Failed to read image")
#                 return
                
#             # Update status while processing
#             self.status_var.set(f"Status: Processing image {os.path.basename(file_path)}...")
#             self.root.update()
            
#             # Extract keypoints and make prediction
#             result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
#             # Save a copy of the processed image for debugging (optional)
#             debug_path = f"debug_{os.path.basename(file_path)}"
#             cv2.imwrite(debug_path, result_image)
            
#             # Update display - make sure image is shown
#             self.display_image(result_image)
#             self.update_results(tamil_char, pronunciation, confidence)
#             self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
#             # Add to history
#             self.add_to_history(tamil_char, pronunciation, confidence)
            
#         except Exception as e:
#             self.status_var.set("Status: Error processing image")
#             error_msg = f"Failed to process image: {str(e)}"
#             print(error_msg)  # Print to console for debugging
#             messagebox.showerror("Error", error_msg)
                
#     def toggle_webcam(self):
#         if not self.model_loaded:
#             messagebox.showerror("Error", "Please load the model and labels first")
#             return
            
#         if self.is_webcam_active:
#             # Stop webcam
#             self.stop_thread = True
#             if self.detection_thread:
#                 self.detection_thread.join(timeout=1.0)
#             if self.cap and self.cap.isOpened():
#                 self.cap.release()
#             self.is_webcam_active = False
#             self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
#             self.capture_btn.config(state=tk.DISABLED)
#             self.status_var.set("Status: Webcam stopped")
#         else:
#             # Start webcam
#             self.cap = cv2.VideoCapture(0)
#             if not self.cap.isOpened():
#                 messagebox.showerror("Error", "Failed to open webcam")
#                 return
                
#             self.is_webcam_active = True
#             self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
#             self.capture_btn.config(state=tk.NORMAL)
#             self.status_var.set("Status: Webcam active")
            
#             # Start detection thread
#             self.stop_thread = False
#             self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
#             self.detection_thread.daemon = True
#             self.detection_thread.start()
            
#     def webcam_detection_loop(self):
#         """Process webcam frames and detect Tamil finger spellings with auto word capture"""
#         prev_char = None
#         stability_count = 0
#         auto_capture_delay = 0  # Counter for auto-capture delay
        
#         while not self.stop_thread and self.cap and self.cap.isOpened():
#             try:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     print("Failed to read from webcam")
#                     break
                    
#                 # Flip the frame horizontally for a more natural view
#                 frame = cv2.flip(frame, 1)
                    
#                 # Extract keypoints and make prediction
#                 result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
#                 # Stability check for display (to reduce flickering)
#                 if tamil_char == prev_char:
#                     stability_count += 1
#                 else:
#                     stability_count = 0
                    
#                 # Only update the display if prediction is stable or very confident
#                 if stability_count >= 3 or confidence > 80:
#                     # Use a lambda with no parameters to ensure thread-safety
#                     self.root.after(0, lambda f=result_frame: self.display_image(f))
#                     self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
#                                     self.update_results(t, p, c))
                    
#                     # If prediction changes with high confidence, add to history
#                     if tamil_char != prev_char and tamil_char and confidence > 65:
#                         self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
#                                         self.add_to_history(t, p, c))
                        
#                     prev_char = tamil_char
                    
#                     # Word recognition logic - track character stability for auto-capture
#                     if self.word_capture_active and tamil_char:
#                         if tamil_char == self.last_detected_char:
#                             self.char_stabilization_count += 1
#                         else:
#                             self.last_detected_char = tamil_char
#                             self.char_stabilization_count = 1
                            
#                             # Reset auto-capture delay when character changes
#                             auto_capture_delay = 0
                        
#                         # Visual feedback for character stability
#                         if self.char_stabilization_count > 0:
#                             # Draw a progress arc on the frame to show stability
#                             center = (result_frame.shape[1] - 50, 50)  # Top-right corner
#                             radius = 30
#                             progress = min(self.char_stabilization_count / self.char_stability_threshold, 1.0)
#                             end_angle = int(360 * progress)
                            
#                             # Draw background circle
#                             cv2.circle(result_frame, center, radius, (50, 50, 50), -1)
                            
#                             # Draw progress arc
#                             if progress < 0.3:
#                                 color = (0, 0, 255)  # Red
#                             elif progress < 0.7:
#                                 color = (0, 255, 255)  # Yellow
#                             else:
#                                 color = (0, 255, 0)  # Green
                                
#                             cv2.ellipse(result_frame, center, (radius, radius), 0, 0, end_angle, color, 5)
                            
#                             # Show in the next frame update
#                             self.root.after(0, lambda f=result_frame: self.display_image(f))
#                 else:
#                     # Just update the display without updating results
#                     self.root.after(0, lambda f=result_frame: self.display_image(f))
                
#                 # Auto-capture logic for word recognition
#                 if self.word_capture_active and tamil_char and self.char_stabilization_count >= self.char_stability_threshold:
#                     # Wait a moment after stability to auto-capture
#                     auto_capture_delay += 1
                    
#                     # If we have a stable character for enough time, auto-capture
#                     if auto_capture_delay >= 20:  # About 2/3 second of stability
#                         # Reset counters
#                         self.char_stabilization_count = 0
#                         auto_capture_delay = 0
                        
#                         # Auto-add the character
#                         self.root.after(0, self.add_current_char_to_word)
                
#                 # Small delay to reduce CPU usage and make UI more responsive
#                 time.sleep(0.03)  # Approximate 30 FPS
                
#             except Exception as e:
#                 print(f"Error in webcam loop: {str(e)}")
#                 time.sleep(0.1)
            
#     def capture_frame(self):
#         if not self.is_webcam_active or not self.cap:
#             return
            
#         ret, frame = self.cap.read()
#         if not ret:
#             messagebox.showerror("Error", "Failed to capture frame")
#             return
            
#         # Flip the frame horizontally for a more natural view
#         frame = cv2.flip(frame, 1)
        
#         # Save the captured frame
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         save_path = f"capture_{timestamp}.jpg"
#         cv2.imwrite(save_path, frame)
        
#         # Process the captured frame
#         result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
#         # Update results
#         self.update_results(tamil_char, pronunciation, confidence)
#         self.add_to_history(tamil_char, pronunciation, confidence)
        
#         # Display notification
#         self.status_var.set(f"Status: Captured frame saved as {save_path}")
#         messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
#     def analyze_image(self, image):
#         """Analyze image and return the recognized Tamil character"""
#         # Extract hand keypoints
#         keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
#         if not hands_detected:
#             return annotated_image, "", "No hands detected", 0.0
            
#         # Predict gesture
#         predicted_class, confidence = self.predict_gesture(keypoints)
        
#         # Get Tamil character and pronunciation
#         if predicted_class in self.tamil_labels:
#             tamil_char = self.tamil_labels[predicted_class]["tamil"]
#             pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
#         else:
#             tamil_char = "?"
#             pronunciation = f"Unknown class: {predicted_class}"
        
#         # Add prediction text to image
#         cv2.putText(annotated_image, pronunciation, (10, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
#         cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 80), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        
#         return annotated_image, tamil_char, pronunciation, confidence
            
#     def extract_hand_keypoints(self, image):
#         """Extract hand keypoints using MediaPipe"""
#         # Convert to RGB for MediaPipe
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
#         # Process image with MediaPipe
#         results = self.hands.process(image_rgb)
        
#         # Initialize placeholders for hand keypoints
#         left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
#         right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
#         # Make a copy of the image for drawing
#         annotated_image = image.copy()
        
#         # Extract keypoints if hands are detected
#         if results.multi_hand_landmarks:
#             for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
#                 hand_keypoints = []
#                 for landmark in hand_landmarks.landmark:
#                     hand_keypoints.append(landmark.x)
#                     hand_keypoints.append(landmark.y)
                
#                 # Assign to left or right hand (simplified for demonstration)
#                 if hand_idx == 0:
#                     left_hand = hand_keypoints
#                 elif hand_idx == 1:
#                     right_hand = hand_keypoints
                
#                 # Draw landmarks on the image
#                 self.mp_drawing.draw_landmarks(
#                     annotated_image,
#                     hand_landmarks,
#                     self.mp_hands.HAND_CONNECTIONS,
#                     self.mp_drawing_styles.get_default_hand_landmarks_style(),
#                     self.mp_drawing_styles.get_default_hand_connections_style()
#                 )
        
#         # Concatenate left & right hand keypoints
#         data_aux = np.concatenate([left_hand, right_hand])
        
#         return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
#     def predict_gesture(self, keypoints):
#         """Predict the Tamil character gesture"""
#         # Reshape input for LSTM: (samples=1, time steps=1, features=84)
#         input_data = keypoints.reshape(1, 1, 84)
        
#         # Make prediction with the model
#         prediction = self.model.predict(input_data, verbose=0)
        
#         # Get the class with highest probability
#         predicted_class = np.argmax(prediction)
#         confidence = np.max(prediction) * 100
        
#         return predicted_class, confidence
            
#     def display_image(self, image):
#         """Display image on canvas with proper scaling"""
#         try:
#             # Convert OpenCV BGR image to RGB for Tkinter
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
#             # Get canvas dimensions
#             canvas_width = self.canvas.winfo_width()
#             canvas_height = self.canvas.winfo_height()
            
#             # If canvas hasn't been fully initialized yet, use default values
#             if canvas_width <= 1 or canvas_height <= 1:
#                 canvas_width = 640  # Default width
#                 canvas_height = 480  # Default height
            
#             # Calculate scaling factor to fit canvas while maintaining aspect ratio
#             img_height, img_width = image_rgb.shape[:2]
#             scale = min(canvas_width/img_width, canvas_height/img_height)
            
#             # New dimensions
#             new_width = int(img_width * scale)
#             new_height = int(img_height * scale)
            
#             # Resize image
#             if scale != 1.0:  # Only resize if needed
#                 image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
#                                       interpolation=cv2.INTER_AREA)
            
#             # Convert to PhotoImage
#             image_pil = Image.fromarray(image_rgb)
#             image_tk = ImageTk.PhotoImage(image=image_pil)
            
#             # Clear previous content and update canvas
#             self.canvas.delete("all")
            
#             # Center the image on the canvas
#             x_offset = max(0, (canvas_width - new_width) // 2)
#             y_offset = max(0, (canvas_height - new_height) // 2)
            
#             # Draw a border around the image area
#             self.canvas.create_rectangle(
#                 x_offset-2, y_offset-2, 
#                 x_offset+new_width+2, y_offset+new_height+2,
#                 outline="#3498db", width=2
#             )
            
#             # Create image
#             self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
#             self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
#             # Force update to ensure image is displayed
#             self.canvas.update()
            
#         except Exception as e:
#             print(f"Error displaying image: {str(e)}")
        
#     def update_results(self, tamil_char, pronunciation, confidence):
#         """Update the results display with enhanced visuals"""
#         self.tamil_char_var.set(tamil_char)
#         self.pronunciation_var.set(pronunciation)
#         self.confidence_var.set(f"{confidence:.2f}%")
#         self.update_confidence_progress(confidence)
        
#         # Highlight the detected character in the reference grid
#         self.highlight_reference_character(tamil_char)

#     def update_confidence_progress(self, confidence):
#         """Update the confidence progress bar"""
#         self.confidence_progress.delete("all")
#         width = self.confidence_progress.winfo_width()
#         if width < 10:  # Not yet properly initialized
#             width = 200
        
#         # Draw the background
#         self.confidence_progress.create_rectangle(0, 0, width, 25, fill="#2c3e50", outline="")
        
#         # Draw the progress bar
#         progress_width = int(width * confidence / 100)
        
#         # Color based on confidence level
#         if confidence < 30:
#             color = "#e74c3c"  # Red for low confidence
#         elif confidence < 70:
#             color = "#f39c12"  # Orange for medium confidence
#         else:
#             color = "#2ecc71"  # Green for high confidence
        
#         self.confidence_progress.create_rectangle(0, 0, progress_width, 25, 
#                                                  fill=color, outline="")
        
#         # Add text
#         self.confidence_progress.create_text(width/2, 13, 
#                                             text=f"{confidence:.2f}%", 
#                                             fill="white", font=("Arial", 12, "bold"))
    
#     def highlight_reference_character(self, tamil_char):
#         """Highlight the detected character in the reference grid"""
#         # Reset all characters to normal background
#         for label in self.reference_labels.values():
#             label.config(bg="#34495e")
        
#         # Highlight the detected character if it exists in our reference grid
#         if tamil_char in self.reference_labels:
#             self.reference_labels[tamil_char].config(bg="#e74c3c")  # Highlight with a red background
        
#     def add_to_history(self, tamil_char, pronunciation, confidence):
#         """Add detection to history"""
#         if not tamil_char:  # Skip empty detections
#             return
            
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
#         # Enable text widget for editing
#         self.history_text.config(state=tk.NORMAL)
        
#         # Insert at the beginning
#         self.history_text.insert("1.0", history_entry)
        
#         # Limit history length
#         if float(self.history_text.index('end-1c').split('.')[0]) > 20:
#             self.history_text.delete("20.0", tk.END)
            
#         # Disable editing
#         self.history_text.config(state=tk.DISABLED)
        
#     def clear_history(self):
#         """Clear detection history"""
#         self.history_text.config(state=tk.NORMAL)
#         self.history_text.delete("1.0", tk.END)
#         self.history_text.config(state=tk.DISABLED)
        
#     def cleanup(self):
#         """Clean up resources before closing"""
#         if self.cap and self.cap.isOpened():
#             self.cap.release()
#         self.stop_thread = True
#         if self.detection_thread:
#             self.detection_thread.join(timeout=1.0)
            
#         # Clean up pygame if initialized
#         if self.pygame_initialized:
#             pygame.mixer.quit()
#             pygame.quit()
            
#         print("Application closed, resources released")

# def create_tamil_label_mapping():
#     """Create the Tamil character label mapping"""
#     # Check if labels file already exists
#     if os.path.exists("tamil_labels.json"):
#         print("Tamil labels file already exists.")
#         return
    
#     # If we needed to create a default Tamil labels file,
#     # we would add that code here. For now, we'll assume
#     # the file is provided by the user.
#     print("Tamil labels file not found. Please provide a valid labels file.")

# def main():
#     # Ensure label mapping file exists
#     create_tamil_label_mapping()
    
#     # Create and run the GUI
#     root = tk.Tk()
#     app = TamilFingerSpellingGUI(root)
    
#     # Set up cleanup on exit
#     root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
#     # Start the GUI event loop
#     root.mainloop()

# if __name__ == "__main__":
#     main()

# import os
# import cv2
# import json
# import pickle
# import numpy as np
# import tensorflow as tf
# import mediapipe as mp
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from tkinter import font as tkfont
# from tensorflow.keras.models import load_model
# from PIL import Image, ImageTk, ImageFont, ImageDraw
# import threading
# from datetime import datetime
# import time
# import platform

# class TamilFingerSpellingGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Tamil Finger Spelling Recognition")
#         self.root.geometry("1200x800")
#         self.root.configure(bg="#2c3e50")
        
#         # Variables
#         self.model = None
#         self.model_loaded = False
#         self.cap = None
#         self.is_webcam_active = False
#         self.detection_thread = None
#         self.stop_thread = False
#         self.tamil_labels = None
        
#         # Setup Tamil fonts
#         self.setup_fonts()
        
#         # Default paths
#         self.default_model_path = "best_lstm_model (3).keras"
#         self.default_labels_path = "tamil_labels.json"
        
#         # MediaPipe setup
#         self.mp_hands = mp.solutions.hands
#         self.mp_drawing = mp.solutions.drawing_utils
#         self.mp_drawing_styles = mp.solutions.drawing_styles
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=2,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5
#         )
        
#         # Create UI elements
#         self.create_widgets()
        
#         # Check for default files
#         self.check_default_files()
        
#     def setup_fonts(self):
#         """Setup fonts for Tamil display"""
#         # Check operating system for appropriate Tamil fonts
#         system = platform.system()
        
#         if system == "Windows":
#             tamil_fonts = ["Latha", "Nirmala UI", "Tamil Sangam MN", "Arial Unicode MS"]
#         elif system == "Darwin":  # macOS
#             tamil_fonts = ["Tamil Sangam MN", "InaiMathi", "Arial Unicode MS"]
#         else:  # Linux and others
#             tamil_fonts = ["Noto Sans Tamil", "Lohit Tamil", "FreeSans", "Arial Unicode MS"]
        
#         # Find first available Tamil font
#         available_fonts = list(tkfont.families())
#         self.tamil_font = None
        
#         for font_name in tamil_fonts:
#             if font_name in available_fonts:
#                 self.tamil_font = font_name
#                 print(f"Using Tamil font: {font_name}")
#                 break
        
#         # If no Tamil font found, use a default font and notify user
#         if not self.tamil_font:
#             self.tamil_font = "TkDefaultFont"
#             print("Warning: No Tamil font found. Install a Tamil font for proper display.")
#             messagebox.showwarning("Font Warning", 
#                 "No Tamil font found. Install a Tamil font like 'Noto Sans Tamil' for proper display.")
    
#     def check_default_files(self):
#         """Check if default model and label files exist and load them"""
#         if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
#             self.model_path_var.set(self.default_model_path)
#             self.labels_path_var.set(self.default_labels_path)
#             self.load_model_and_labels()
        
#     def create_widgets(self):
#         # Main frames layout - Using a different approach for better balance
#         self.main_frame = tk.Frame(self.root, bg="#2c3e50")
#         self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Create a 2x2 grid layout
#         self.main_frame.columnconfigure(0, weight=1, minsize=300)  # Control column
#         self.main_frame.columnconfigure(1, weight=3, minsize=600)  # Display column
#         self.main_frame.rowconfigure(0, weight=1)  # Top row
#         self.main_frame.rowconfigure(1, weight=1)  # Bottom row
        
#         # Create four main sections in the grid
#         self.top_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
#         self.top_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
#         self.bottom_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
#         self.bottom_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
        
#         # Place frames in the grid
#         self.top_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
#         self.top_right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
#         self.bottom_left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
#         self.bottom_right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
#         # Title and logo in top left
#         title_frame = tk.Frame(self.top_left_frame, bg="#34495e")
#         title_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(title_frame, text="Tamil Finger Spelling", 
#                 font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=2)
#         tk.Label(title_frame, text="Recognition System", 
#                 font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
#         # *** DETECTION RESULTS in top left (below title) ***
#         self.enhance_results_frame(self.top_left_frame)
        
#         # *** MODEL SETTINGS in bottom left ***
#         # Model and labels loading section
#         files_frame = tk.LabelFrame(self.bottom_left_frame, text="Model & Labels", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         files_frame.pack(fill=tk.X, pady=5)
        
#         # Model path
#         tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
#         self.model_path_var = tk.StringVar()
#         self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
#         self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
#         self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
#                                          bg="#3498db", fg="white", width=6)
#         self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
#         # Labels path
#         tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
#         self.labels_path_var = tk.StringVar()
#         self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
#         self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
#         self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
#                                           bg="#3498db", fg="white", width=6)
#         self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
#         # Load button
#         self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
#                                  command=self.load_model_and_labels,
#                                  bg="#2ecc71", fg="white", width=15, height=2)
#         self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
#         # *** INPUT OPTIONS in bottom left (below model settings) ***
#         # Input options section
#         input_frame = tk.LabelFrame(self.bottom_left_frame, text="Input Options", 
#                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         input_frame.pack(fill=tk.X, pady=5)
        
#         button_frame = tk.Frame(input_frame, bg="#34495e")
#         button_frame.pack(fill=tk.X)
        
#         # Create a grid for better button layout
#         button_frame.columnconfigure(0, weight=1)
#         button_frame.columnconfigure(1, weight=1)
        
#         self.image_btn = tk.Button(button_frame, text="Upload Image", command=self.process_image, 
#                                   bg="#e74c3c", fg="white", width=15, height=2, state=tk.DISABLED)
#         self.image_btn.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        
#         self.webcam_btn = tk.Button(button_frame, text="Start Webcam", command=self.toggle_webcam, 
#                                    bg="#9b59b6", fg="white", width=15, height=2, state=tk.DISABLED)
#         self.webcam_btn.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
#         self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
#                                     bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
#         self.capture_btn.pack(pady=5)
        
#         # Detection parameters section
#         params_frame = tk.LabelFrame(self.bottom_left_frame, text="Detection Parameters", 
#                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=5)
#         params_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
#         self.confidence_threshold = tk.DoubleVar(value=0.5)
#         confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
#                                      variable=self.confidence_threshold, 
#                                      orient=tk.HORIZONTAL, length=200)
#         confidence_scale.pack(fill=tk.X, pady=5)
        
#         # Create a label to display the current value
#         self.threshold_value_label = tk.Label(params_frame, text="0.5", bg="#34495e", fg="white")
#         self.threshold_value_label.pack(anchor=tk.E)
        
#         # Update label when scale changes
#         confidence_scale.bind("<Motion>", self.update_threshold_label)
        
#         # *** CAMERA VIEW in top right ***
#         # Display frame elements - Taking most of the right side
#         camera_frame = tk.LabelFrame(self.top_right_frame, text="Camera View", 
#                                     font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
#         camera_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
#         self.canvas = tk.Canvas(camera_frame, bg="black", width=640, height=480)
#         self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
#         # *** HISTORY and REFERENCE in bottom right ***
#         # Bottom right area split into two sections
#         ref_history_frame = tk.Frame(self.bottom_right_frame, bg="#2c3e50")
#         ref_history_frame.pack(fill=tk.BOTH, expand=True)
        
#         # History section
#         history_frame = tk.LabelFrame(ref_history_frame, text="Detection History", 
#                                      font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
#         history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         self.history_text = tk.Text(history_frame, width=25, height=10, bg="#2c3e50", fg="white",
#                                    font=("Arial", 10))
#         self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)
#         self.history_text.config(state=tk.DISABLED)
        
#         # Clear button
#         self.clear_btn = tk.Button(history_frame, text="Clear History", 
#                                   command=self.clear_history,
#                                   bg="#7f8c8d", fg="white")
#         self.clear_btn.pack(pady=5)
        
#         # Reference section
#         reference_frame = tk.LabelFrame(ref_history_frame, text="Reference", 
#                                         font=("Arial", 12), bg="#2c3e50", fg="white")
#         reference_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Reference grid (will be populated with character references)
#         self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=150)
#         self.reference_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Status bar
#         self.status_var = tk.StringVar(value="Status: Ready")
#         self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
#                                   font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
#                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
#     def enhance_results_frame(self, parent_frame):
#         """Enhanced results frame with larger Tamil character display"""
#         # Results section with improved visibility
#         self.results_frame = tk.LabelFrame(parent_frame, text="Detection Results", 
#                                           font=("Arial", 16, "bold"), bg="#34495e", fg="#f39c12", 
#                                           padx=15, pady=10, relief=tk.RAISED, bd=3)
#         self.results_frame.pack(fill=tk.X, pady=5)
        
#         # Create a frame with a distinct background for the Tamil character
#         char_display_frame = tk.Frame(self.results_frame, bg="#1c2e3c", 
#                                      padx=15, pady=10, relief=tk.RAISED, bd=3)
#         char_display_frame.pack(fill=tk.X, pady=5)
        
#         # Tamil character display - Large but not too large
#         self.tamil_char_var = tk.StringVar(value="")
#         self.tamil_char_label = tk.Label(char_display_frame, textvariable=self.tamil_char_var,
#                                         font=(self.tamil_font, 120), bg="#1c2e3c", fg="#ecf0f1",
#                                         height=1)
#         self.tamil_char_label.pack(pady=5)
        
#         # Pronunciation with better formatting
#         pronunciation_frame = tk.Frame(self.results_frame, bg="#34495e")
#         pronunciation_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(pronunciation_frame, text="Pronunciation:", 
#                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
#         self.pronunciation_var = tk.StringVar(value="No detection yet")
#         self.pronunciation_label = tk.Label(pronunciation_frame, textvariable=self.pronunciation_var, 
#                                           font=("Arial", 12), bg="#34495e", fg="white")
#         self.pronunciation_label.pack(side=tk.LEFT, padx=5)
        
#         # Confidence with progress bar
#         confidence_frame = tk.Frame(self.results_frame, bg="#34495e")
#         confidence_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(confidence_frame, text="Confidence:", 
#                 font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
#         self.confidence_var = tk.StringVar(value="0.00%")
#         self.confidence_label = tk.Label(confidence_frame, textvariable=self.confidence_var, 
#                                         font=("Arial", 12), bg="#34495e", fg="white")
#         self.confidence_label.pack(side=tk.LEFT, padx=5)
        
#         # Add a progress bar for confidence
#         self.confidence_progress_frame = tk.Frame(self.results_frame, bg="#34495e", height=25)
#         self.confidence_progress_frame.pack(fill=tk.X, pady=5)
        
#         self.confidence_progress = tk.Canvas(self.confidence_progress_frame, 
#                                             bg="#2c3e50", height=25, bd=0, highlightthickness=0)
#         self.confidence_progress.pack(fill=tk.X)
    
#     def update_threshold_label(self, event=None):
#         """Update the threshold value label"""
#         self.threshold_value_label.config(text=f"{self.confidence_threshold.get():.1f}")
        
#     def browse_model(self):
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("Keras Model", "*.keras"), 
#             ("H5 Model", "*.h5"),
#             ("All Files", "*.*")
#         ])
#         if file_path:
#             self.model_path_var.set(file_path)
            
#     def browse_labels(self):
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("JSON Files", "*.json"),
#             ("All Files", "*.*")
#         ])
#         if file_path:
#             self.labels_path_var.set(file_path)
            
#     def load_model_and_labels(self):
#         model_path = self.model_path_var.get()
#         labels_path = self.labels_path_var.get()
        
#         if not model_path:
#             messagebox.showerror("Error", "Please select a model file")
#             return
            
#         if not labels_path:
#             messagebox.showerror("Error", "Please select a labels file")
#             return
            
#         if not os.path.exists(model_path):
#             messagebox.showerror("Error", f"Model file not found: {model_path}")
#             return
            
#         if not os.path.exists(labels_path):
#             messagebox.showerror("Error", f"Labels file not found: {labels_path}")
#             return
            
#         try:
#             self.status_var.set("Status: Loading model and labels...")
#             self.root.update()
            
#             # Load the model
#             self.model = load_model(model_path)
            
#             # Load the Tamil labels
#             with open(labels_path, 'r', encoding='utf-8') as f:
#                 self.tamil_labels = json.load(f)
            
#             # Convert string keys to integers
#             self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
#             self.model_loaded = True
            
#             # Enable buttons
#             self.image_btn.config(state=tk.NORMAL)
#             self.webcam_btn.config(state=tk.NORMAL)
            
#             # Update status
#             self.status_var.set("Status: Model and labels loaded successfully")
#             messagebox.showinfo("Success", "Model and labels loaded successfully")
            
#             # Create reference grid
#             self.create_reference_grid()
            
#         except Exception as e:
#             self.status_var.set(f"Status: Error loading model or labels")
#             messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
#     def create_reference_grid(self):
#         """Create a scrollable grid of reference Tamil characters"""
#         # Clear existing content
#         self.reference_canvas.delete("all")
        
#         # Create a frame inside the canvas to hold the characters
#         frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
#         self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
#         # Add characters in a grid (10 per row)
#         row, col = 0, 0
#         self.reference_labels = {}  # Store references to labels for highlighting
        
#         for char_id in sorted(self.tamil_labels.keys()):
#             if char_id == 247:  # Skip background class (if applicable)
#                 continue
                
#             # Create frame for each character
#             char_frame = tk.Frame(frame, bg="#34495e", width=60, height=60, 
#                                  padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
#             char_frame.grid(row=row, column=col, padx=3, pady=3)
#             char_frame.grid_propagate(False)  # Keep fixed size
            
#             # Add Tamil character with improved font
#             char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
#                                  font=(self.tamil_font, 16), bg="#34495e", fg="white")
#             char_label.pack(expand=True)
            
#             # Store reference to this label
#             self.reference_labels[self.tamil_labels[char_id]["tamil"]] = char_label
            
#             # Tooltip with pronunciation
#             self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
#             # Update row and column
#             col += 1
#             if col >= 8:  # Reduce columns to fit better
#                 col = 0
#                 row += 1
        
#         # Update the canvas scroll region
#         frame.update_idletasks()
#         self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
#         # Add scrollbar
#         scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
#                                 command=self.reference_canvas.xview)
#         self.reference_canvas.config(xscrollcommand=scrollbar.set)
#         scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
#     def create_tooltip(self, widget, text):
#         """Create a tooltip for a widget"""
#         def enter(event):
#             # Create a new tooltip window when mouse enters
#             tooltip = tk.Toplevel(widget)
#             tooltip.wm_overrideredirect(True)  # Remove window decorations
            
#             # Create label inside the tooltip window
#             label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
#             label.pack()
            
#             # Position the tooltip near the widget
#             x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
#             x += widget.winfo_rootx() + 25
#             y += widget.winfo_rooty() + 25
#             tooltip.wm_geometry(f"+{x}+{y}")
            
#             # Store the tooltip reference on the widget
#             widget.tooltip = tooltip
            
#         def leave(event):
#             # Destroy the tooltip when mouse leaves
#             if hasattr(widget, 'tooltip'):
#                 widget.tooltip.destroy()
#                 delattr(widget, 'tooltip')
            
#         # Bind events
#         widget.bind("<Enter>", enter)
#         widget.bind("<Leave>", leave)
    
#     def process_image(self):
#         if not self.model_loaded:
#             messagebox.showerror("Error", "Please load the model and labels first")
#             return
            
#         file_path = filedialog.askopenfilename(filetypes=[
#             ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
#             ("All Files", "*.*")
#         ])
        
#         if not file_path:
#             return
            
#         try:
#             # Read image
#             image = cv2.imread(file_path)
            
#             if image is None:
#                 messagebox.showerror("Error", "Failed to read image")
#                 return
                
#             # Update status while processing
#             self.status_var.set(f"Status: Processing image {os.path.basename(file_path)}...")
#             self.root.update()
            
#             # Extract keypoints and make prediction
#             result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
#             # Save a copy of the processed image for debugging (optional)
#             debug_path = f"debug_{os.path.basename(file_path)}"
#             cv2.imwrite(debug_path, result_image)
            
#             # Update display - make sure image is shown
#             self.display_image(result_image)
#             self.update_results(tamil_char, pronunciation, confidence)
#             self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
#             # Add to history
#             self.add_to_history(tamil_char, pronunciation, confidence)
            
#         except Exception as e:
#             self.status_var.set("Status: Error processing image")
#             error_msg = f"Failed to process image: {str(e)}"
#             print(error_msg)  # Print to console for debugging
#             messagebox.showerror("Error", error_msg)
                
#     def toggle_webcam(self):
#         if not self.model_loaded:
#             messagebox.showerror("Error", "Please load the model and labels first")
#             return
            
#         if self.is_webcam_active:
#             # Stop webcam
#             self.stop_thread = True
#             if self.detection_thread:
#                 self.detection_thread.join(timeout=1.0)
#             if self.cap and self.cap.isOpened():
#                 self.cap.release()
#             self.is_webcam_active = False
#             self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
#             self.capture_btn.config(state=tk.DISABLED)
#             self.status_var.set("Status: Webcam stopped")
#         else:
#             # Start webcam
#             self.cap = cv2.VideoCapture(0)
#             if not self.cap.isOpened():
#                 messagebox.showerror("Error", "Failed to open webcam")
#                 return
                
#             self.is_webcam_active = True
#             self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
#             self.capture_btn.config(state=tk.NORMAL)
#             self.status_var.set("Status: Webcam active")
            
#             # Start detection thread
#             self.stop_thread = False
#             self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
#             self.detection_thread.daemon = True
#             self.detection_thread.start()
            
#     def webcam_detection_loop(self):
#         """Process webcam frames and detect Tamil finger spellings"""
#         prev_char = None
#         stability_count = 0
        
#         while not self.stop_thread and self.cap and self.cap.isOpened():
#             try:
#                 ret, frame = self.cap.read()
#                 if not ret:
#                     print("Failed to read from webcam")
#                     break
                    
#                 # Flip the frame horizontally for a more natural view
#                 frame = cv2.flip(frame, 1)
                    
#                 # Extract keypoints and make prediction
#                 result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
#                 # Stability check (to reduce flickering)
#                 if tamil_char == prev_char:
#                     stability_count += 1
#                 else:
#                     stability_count = 0
                    
#                 # Only update the display if prediction is stable or very confident
#                 if stability_count >= 3 or confidence > 80:
#                     # Use a lambda with no parameters to ensure thread-safety
#                     self.root.after(0, lambda f=result_frame: self.display_image(f))
#                     self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
#                                     self.update_results(t, p, c))
                    
#                     # If prediction changes with high confidence, add to history
#                     if tamil_char != prev_char and tamil_char and confidence > 65:
#                         self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
#                                         self.add_to_history(t, p, c))
                        
#                     prev_char = tamil_char
#                 else:
#                     # Just update the display without updating results
#                     self.root.after(0, lambda f=result_frame: self.display_image(f))
                
#                 # Small delay to reduce CPU usage and make UI more responsive
#                 time.sleep(0.03)  # Approximate 30 FPS
                
#             except Exception as e:
#                 print(f"Error in webcam loop: {str(e)}")
#                 time.sleep(0.1)
            
#     def capture_frame(self):
#         if not self.is_webcam_active or not self.cap:
#             return
            
#         ret, frame = self.cap.read()
#         if not ret:
#             messagebox.showerror("Error", "Failed to capture frame")
#             return
            
#         # Flip the frame horizontally for a more natural view
#         frame = cv2.flip(frame, 1)
        
#         # Save the captured frame
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         save_path = f"capture_{timestamp}.jpg"
#         cv2.imwrite(save_path, frame)
        
#         # Process the captured frame
#         result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
#         # Update results
#         self.update_results(tamil_char, pronunciation, confidence)
#         self.add_to_history(tamil_char, pronunciation, confidence)
        
#         # Display notification
#         self.status_var.set(f"Status: Captured frame saved as {save_path}")
#         messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
#     def analyze_image(self, image):
#         """Analyze image and return the recognized Tamil character"""
#         # Extract hand keypoints
#         keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
#         if not hands_detected:
#             return annotated_image, "", "No hands detected", 0.0
            
#         # Predict gesture
#         predicted_class, confidence = self.predict_gesture(keypoints)
        
#         # Get Tamil character and pronunciation
#         if predicted_class in self.tamil_labels:
#             tamil_char = self.tamil_labels[predicted_class]["tamil"]
#             pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
#         else:
#             tamil_char = "?"
#             pronunciation = f"Unknown class: {predicted_class}"
        
#         # Add prediction text to image
#         cv2.putText(annotated_image, pronunciation, (10, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
#         cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 80), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        
#         return annotated_image, tamil_char, pronunciation, confidence
            
#     def extract_hand_keypoints(self, image):
#         """Extract hand keypoints using MediaPipe"""
#         # Convert to RGB for MediaPipe
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
#         # Process image with MediaPipe
#         results = self.hands.process(image_rgb)
        
#         # Initialize placeholders for hand keypoints
#         left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
#         right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
#         # Make a copy of the image for drawing
#         annotated_image = image.copy()
        
#         # Extract keypoints if hands are detected
#         if results.multi_hand_landmarks:
#             for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
#                 hand_keypoints = []
#                 for landmark in hand_landmarks.landmark:
#                     hand_keypoints.append(landmark.x)
#                     hand_keypoints.append(landmark.y)
                
#                 # Assign to left or right hand (simplified for demonstration)
#                 if hand_idx == 0:
#                     left_hand = hand_keypoints
#                 elif hand_idx == 1:
#                     right_hand = hand_keypoints
                
#                 # Draw landmarks on the image
#                 self.mp_drawing.draw_landmarks(
#                     annotated_image,
#                     hand_landmarks,
#                     self.mp_hands.HAND_CONNECTIONS,
#                     self.mp_drawing_styles.get_default_hand_landmarks_style(),
#                     self.mp_drawing_styles.get_default_hand_connections_style()
#                 )
        
#         # Concatenate left & right hand keypoints
#         data_aux = np.concatenate([left_hand, right_hand])
        
#         return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
#     def predict_gesture(self, keypoints):
#         """Predict the Tamil character gesture"""
#         # Reshape input for LSTM: (samples=1, time steps=1, features=84)
#         input_data = keypoints.reshape(1, 1, 84)
        
#         # Make prediction with the model
#         prediction = self.model.predict(input_data, verbose=0)
        
#         # Get the class with highest probability
#         predicted_class = np.argmax(prediction)
#         confidence = np.max(prediction) * 100
        
#         return predicted_class, confidence
            
#     def display_image(self, image):
#         """Display image on canvas with proper scaling"""
#         try:
#             # Convert OpenCV BGR image to RGB for Tkinter
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
#             # Get canvas dimensions
#             canvas_width = self.canvas.winfo_width()
#             canvas_height = self.canvas.winfo_height()
            
#             # If canvas hasn't been fully initialized yet, use default values
#             if canvas_width <= 1 or canvas_height <= 1:
#                 canvas_width = 640  # Default width
#                 canvas_height = 480  # Default height
            
#             # Calculate scaling factor to fit canvas while maintaining aspect ratio
#             img_height, img_width = image_rgb.shape[:2]
#             scale = min(canvas_width/img_width, canvas_height/img_height)
            
#             # New dimensions
#             new_width = int(img_width * scale)
#             new_height = int(img_height * scale)
            
#             # Resize image
#             if scale != 1.0:  # Only resize if needed
#                 image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
#                                       interpolation=cv2.INTER_AREA)
            
#             # Convert to PhotoImage
#             image_pil = Image.fromarray(image_rgb)
#             image_tk = ImageTk.PhotoImage(image=image_pil)
            
#             # Clear previous content and update canvas
#             self.canvas.delete("all")
            
#             # Center the image on the canvas
#             x_offset = max(0, (canvas_width - new_width) // 2)
#             y_offset = max(0, (canvas_height - new_height) // 2)
            
#             # Draw a border around the image area
#             self.canvas.create_rectangle(
#                 x_offset-2, y_offset-2, 
#                 x_offset+new_width+2, y_offset+new_height+2,
#                 outline="#3498db", width=2
#             )
            
#             # Create image
#             self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
#             self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
#             # Force update to ensure image is displayed
#             self.canvas.update()
            
#         except Exception as e:
#             print(f"Error displaying image: {str(e)}")
        
#     def update_results(self, tamil_char, pronunciation, confidence):
#         """Update the results display with enhanced visuals"""
#         self.tamil_char_var.set(tamil_char)
#         self.pronunciation_var.set(pronunciation)
#         self.confidence_var.set(f"{confidence:.2f}%")
#         self.update_confidence_progress(confidence)
        
#         # Highlight the detected character in the reference grid
#         self.highlight_reference_character(tamil_char)

#     def update_confidence_progress(self, confidence):
#         """Update the confidence progress bar"""
#         self.confidence_progress.delete("all")
#         width = self.confidence_progress.winfo_width()
#         if width < 10:  # Not yet properly initialized
#             width = 200
        
#         # Draw the background
#         self.confidence_progress.create_rectangle(0, 0, width, 25, fill="#2c3e50", outline="")
        
#         # Draw the progress bar
#         progress_width = int(width * confidence / 100)
        
#         # Color based on confidence level
#         if confidence < 30:
#             color = "#e74c3c"  # Red for low confidence
#         elif confidence < 70:
#             color = "#f39c12"  # Orange for medium confidence
#         else:
#             color = "#2ecc71"  # Green for high confidence
        
#         self.confidence_progress.create_rectangle(0, 0, progress_width, 25, 
#                                                  fill=color, outline="")
        
#         # Add text
#         self.confidence_progress.create_text(width/2, 13, 
#                                             text=f"{confidence:.2f}%", 
#                                             fill="white", font=("Arial", 12, "bold"))
    
#     def highlight_reference_character(self, tamil_char):
#         """Highlight the detected character in the reference grid"""
#         # Reset all characters to normal background
#         for label in self.reference_labels.values():
#             label.config(bg="#34495e")
        
#         # Highlight the detected character if it exists in our reference grid
#         if tamil_char in self.reference_labels:
#             self.reference_labels[tamil_char].config(bg="#e74c3c")  # Highlight with a red background
        
#     def add_to_history(self, tamil_char, pronunciation, confidence):
#         """Add detection to history"""
#         if not tamil_char:  # Skip empty detections
#             return
            
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
#         # Enable text widget for editing
#         self.history_text.config(state=tk.NORMAL)
        
#         # Insert at the beginning
#         self.history_text.insert("1.0", history_entry)
        
#         # Limit history length
#         if float(self.history_text.index('end-1c').split('.')[0]) > 20:
#             self.history_text.delete("20.0", tk.END)
            
#         # Disable editing
#         self.history_text.config(state=tk.DISABLED)
        
#     def clear_history(self):
#         """Clear detection history"""
#         self.history_text.config(state=tk.NORMAL)
#         self.history_text.delete("1.0", tk.END)
#         self.history_text.config(state=tk.DISABLED)
        
#     def cleanup(self):
#         """Clean up resources before closing"""
#         if self.cap and self.cap.isOpened():
#             self.cap.release()
#         self.stop_thread = True
#         if self.detection_thread:
#             self.detection_thread.join(timeout=1.0)
#         print("Application closed, resources released")

# def create_tamil_label_mapping():
#     """Create the Tamil character label mapping"""
#     # Check if labels file already exists
#     if os.path.exists("tamil_labels.json"):
#         print("Tamil labels file already exists.")
#         return
    
#     # If we needed to create a default Tamil labels file,
#     # we would add that code here. For now, we'll assume
#     # the file is provided by the user.
#     print("Tamil labels file not found. Please provide a valid labels file.")

# def main():
#     # Ensure label mapping file exists
#     create_tamil_label_mapping()
    
#     # Create and run the GUI
#     root = tk.Tk()
#     app = TamilFingerSpellingGUI(root)
    
#     # Set up cleanup on exit
#     root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
#     # Start the GUI event loop
#     root.mainloop()

# if __name__ == "__main__":
#     main()

import os
import cv2
import json
import pickle
import numpy as np
import tensorflow as tf
import mediapipe as mp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk, ImageFont, ImageDraw
import threading
from datetime import datetime
import time
import platform
import random

# Constants for word practice
COMMON_WORDS = {
    "Hi/Hello": [188, 92, 14, 32, 23],
    "Sorry (மன்னிக்கவும்)": [140, 31, 238, 14, 32, 192, 23],  # Mannikkavum
    "Please (தயவுசெய்து)": [104, 152, 192, 62, 24, 108]      # Tayavuceytu
}

class TamilFingerSpellingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamil Finger Spelling Recognition")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # Variables
        self.model = None
        self.model_loaded = False
        self.cap = None
        self.is_webcam_active = False
        self.detection_thread = None
        self.stop_thread = False
        self.tamil_labels = None
        
        # Game state variables
        self.current_guessing_image = None
        self.current_guessing_answer = None
        self.current_score = 0
        self.total_attempts = 0
        
        # Word practice variables
        self.current_practice_word = None
        self.current_word_chars = []
        self.current_char_index = 0
        self.word_practice_active = False
        self.last_char_time = 0
        self.char_recognized_time = 0
        self.char_hold_duration = 0
        
        # Setup Tamil fonts
        self.setup_fonts()
        
        # Default paths
        self.default_model_path = "best_lstm_model (3).keras"
        self.default_labels_path = "tamil_labels.json"
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Show main menu
        self.show_main_menu()
        
    def setup_fonts(self):
        """Setup fonts for Tamil display"""
        # Check operating system for appropriate Tamil fonts
        system = platform.system()
        
        if system == "Windows":
            tamil_fonts = ["Latha", "Nirmala UI", "Tamil Sangam MN", "Arial Unicode MS"]
        elif system == "Darwin":  # macOS
            tamil_fonts = ["Tamil Sangam MN", "InaiMathi", "Arial Unicode MS"]
        else:  # Linux and others
            tamil_fonts = ["Noto Sans Tamil", "Lohit Tamil", "FreeSans", "Arial Unicode MS"]
        
        # Find first available Tamil font
        available_fonts = list(tkfont.families())
        self.tamil_font = None
        
        for font_name in tamil_fonts:
            if font_name in available_fonts:
                self.tamil_font = font_name
                print(f"Using Tamil font: {font_name}")
                break
        
        # If no Tamil font found, use a default font and notify user
        if not self.tamil_font:
            self.tamil_font = "TkDefaultFont"
            print("Warning: No Tamil font found. Install a Tamil font for proper display.")
            messagebox.showwarning("Font Warning", 
                "No Tamil font found. Install a Tamil font like 'Noto Sans Tamil' for proper display.")
    
    def show_main_menu(self):
        """Create and show the main menu for mode selection"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main menu frame
        menu_frame = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=20)
        menu_frame.pack(expand=True)
        
        # Title
        title_label = tk.Label(menu_frame, text="Tamil Finger Spelling Recognition", 
                              font=("Arial", 24, "bold"), bg="#2c3e50", fg="white", pady=20)
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(menu_frame, text="Select a mode to continue", 
                              font=("Arial", 16), bg="#2c3e50", fg="#bdc3c7", pady=10)
        subtitle_label.pack()
        
        # Buttons for different modes
        button_width = 30
        button_height = 3
        button_styles = {
            "font": ("Arial", 14, "bold"),
            "bd": 0,
            "relief": tk.FLAT,
            "pady": 10,
        }
        
        # Character Recognition button
        char_button = tk.Button(menu_frame, text="Character Recognition", 
                              command=self.start_character_recognition,
                              bg="#3498db", fg="white", width=button_width, height=button_height,
                              **button_styles)
        char_button.pack(pady=10)
        
        # Word Practice button
        word_button = tk.Button(menu_frame, text="Word Practice", 
                              command=self.start_word_practice,
                              bg="#2ecc71", fg="white", width=button_width, height=button_height,
                              **button_styles)
        word_button.pack(pady=10)
        
        # Guessing Game button
        game_button = tk.Button(menu_frame, text="Character Guessing Game", 
                              command=self.start_guessing_game,
                              bg="#e74c3c", fg="white", width=button_width, height=button_height,
                              **button_styles)
        game_button.pack(pady=10)
        
        # Load model first notification
        note_label = tk.Label(menu_frame, text="Note: Model will be loaded when you select a mode", 
                           font=("Arial", 12, "italic"), bg="#2c3e50", fg="#95a5a6", pady=20)
        note_label.pack()
        
        # Version info
        version_label = tk.Label(menu_frame, text="v2.0", 
                                font=("Arial", 10), bg="#2c3e50", fg="#7f8c8d")
        version_label.pack(side=tk.BOTTOM, pady=10)
    
    def start_character_recognition(self):
        """Initialize and start the character recognition mode"""
        # Clear main menu
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main frames and UI elements
        self.create_recognition_ui()
        
        # Check for default files and load model
        self.check_default_files()
    
    def check_default_files(self):
        """Check if default model and label files exist and load them"""
        if os.path.exists(self.default_model_path) and os.path.exists(self.default_labels_path):
            self.model_path_var.set(self.default_model_path)
            self.labels_path_var.set(self.default_labels_path)
            self.load_model_and_labels()
        
    def create_recognition_ui(self):
        """Create the UI for character recognition mode"""
        # Main frames layout - Using a different approach for better balance
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a 2x2 grid layout
        self.main_frame.columnconfigure(0, weight=1, minsize=300)  # Control column
        self.main_frame.columnconfigure(1, weight=3, minsize=600)  # Display column
        self.main_frame.rowconfigure(0, weight=1)  # Top row
        self.main_frame.rowconfigure(1, weight=1)  # Bottom row
        
        # Create four main sections in the grid
        self.top_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
        self.top_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
        self.bottom_left_frame = tk.Frame(self.main_frame, bg="#34495e", padx=10, pady=10)
        self.bottom_right_frame = tk.Frame(self.main_frame, bg="#2c3e50", padx=10, pady=10)
        
        # Place frames in the grid
        self.top_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.top_right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.bottom_left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.bottom_right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Title and logo in top left
        title_frame = tk.Frame(self.top_left_frame, bg="#34495e")
        title_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(title_frame, text="Tamil Finger Spelling", 
                font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=2)
        tk.Label(title_frame, text="Recognition System", 
                font=("Arial", 14), bg="#34495e", fg="white").pack(pady=2)
        
        # Back to main menu button
        back_btn = tk.Button(title_frame, text="Main Menu", command=self.show_main_menu,
                            bg="#7f8c8d", fg="white", padx=10)
        back_btn.pack(pady=5)
        
        # *** DETECTION RESULTS in top left (below title) ***
        self.enhance_results_frame(self.top_left_frame)
        
        # *** MODEL SETTINGS in bottom left ***
        # Model and labels loading section
        files_frame = tk.LabelFrame(self.bottom_left_frame, text="Model & Labels", 
                                   font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
        files_frame.pack(fill=tk.X, pady=5)
        
        # Model path
        tk.Label(files_frame, text="Model Path:", bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.model_path_var = tk.StringVar()
        self.model_path_entry = tk.Entry(files_frame, textvariable=self.model_path_var, width=20)
        self.model_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.browse_model_btn = tk.Button(files_frame, text="Browse", command=self.browse_model, 
                                         bg="#3498db", fg="white", width=6)
        self.browse_model_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Labels path
        tk.Label(files_frame, text="Labels Path:", bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.labels_path_var = tk.StringVar()
        self.labels_path_entry = tk.Entry(files_frame, textvariable=self.labels_path_var, width=20)
        self.labels_path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.browse_labels_btn = tk.Button(files_frame, text="Browse", command=self.browse_labels, 
                                          bg="#3498db", fg="white", width=6)
        self.browse_labels_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Load button
        self.load_btn = tk.Button(files_frame, text="Load Model & Labels", 
                                 command=self.load_model_and_labels,
                                 bg="#2ecc71", fg="white", width=15, height=2)
        self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # *** INPUT OPTIONS in bottom left (below model settings) ***
        # Input options section
        input_frame = tk.LabelFrame(self.bottom_left_frame, text="Input Options", 
                                   font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=5)
        
        button_frame = tk.Frame(input_frame, bg="#34495e")
        button_frame.pack(fill=tk.X)
        
        # Create a grid for better button layout
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.image_btn = tk.Button(button_frame, text="Upload Image", command=self.process_image, 
                                  bg="#e74c3c", fg="white", width=15, height=2, state=tk.DISABLED)
        self.image_btn.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        
        self.webcam_btn = tk.Button(button_frame, text="Start Webcam", command=self.toggle_webcam, 
                                   bg="#9b59b6", fg="white", width=15, height=2, state=tk.DISABLED)
        self.webcam_btn.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        self.capture_btn = tk.Button(input_frame, text="Capture Frame", command=self.capture_frame, 
                                    bg="#f39c12", fg="white", width=20, height=2, state=tk.DISABLED)
        self.capture_btn.pack(pady=5)
        
        # Detection parameters section
        params_frame = tk.LabelFrame(self.bottom_left_frame, text="Detection Parameters", 
                                    font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=5)
        params_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(params_frame, text="Confidence Threshold:", bg="#34495e", fg="white").pack(anchor=tk.W)
        self.confidence_threshold = tk.DoubleVar(value=0.5)
        confidence_scale = ttk.Scale(params_frame, from_=0.1, to=0.9, 
                                     variable=self.confidence_threshold, 
                                     orient=tk.HORIZONTAL, length=200)
        confidence_scale.pack(fill=tk.X, pady=5)
        
        # Create a label to display the current value
        self.threshold_value_label = tk.Label(params_frame, text="0.5", bg="#34495e", fg="white")
        self.threshold_value_label.pack(anchor=tk.E)
        
        # Update label when scale changes
        confidence_scale.bind("<Motion>", self.update_threshold_label)
        
        # *** CAMERA VIEW in top right ***
        # Display frame elements - Taking most of the right side
        camera_frame = tk.LabelFrame(self.top_right_frame, text="Camera View", 
                                    font=("Arial", 12, "bold"), bg="#2c3e50", fg="white")
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(camera_frame, bg="black", width=640, height=480)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # *** HISTORY and REFERENCE in bottom right ***
        # Bottom right area split into two sections
        ref_history_frame = tk.Frame(self.bottom_right_frame, bg="#2c3e50")
        ref_history_frame.pack(fill=tk.BOTH, expand=True)
        
        # History section
        history_frame = tk.LabelFrame(ref_history_frame, text="Detection History", 
                                     font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=10)
        history_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.history_text = tk.Text(history_frame, width=25, height=10, bg="#2c3e50", fg="white",
                                   font=("Arial", 10))
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.history_text.config(state=tk.DISABLED)
        
        # Clear button
        self.clear_btn = tk.Button(history_frame, text="Clear History", 
                                  command=self.clear_history,
                                  bg="#7f8c8d", fg="white")
        self.clear_btn.pack(pady=5)
        
        # Reference section
        reference_frame = tk.LabelFrame(ref_history_frame, text="Reference", 
                                        font=("Arial", 12), bg="#2c3e50", fg="white")
        reference_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Reference grid (will be populated with character references)
        self.reference_canvas = tk.Canvas(reference_frame, bg="#2c3e50", height=150)
        self.reference_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Status: Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                  font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def enhance_results_frame(self, parent_frame):
        """Enhanced results frame with larger Tamil character display"""
        # Results section with improved visibility
        self.results_frame = tk.LabelFrame(parent_frame, text="Detection Results", 
                                          font=("Arial", 16, "bold"), bg="#34495e", fg="#f39c12", 
                                          padx=15, pady=10, relief=tk.RAISED, bd=3)
        self.results_frame.pack(fill=tk.X, pady=5)
        
        # Create a frame with a distinct background for the Tamil character
        char_display_frame = tk.Frame(self.results_frame, bg="#1c2e3c", 
                                     padx=15, pady=10, relief=tk.RAISED, bd=3)
        char_display_frame.pack(fill=tk.X, pady=5)
        
        # Tamil character display - Large but not too large
        self.tamil_char_var = tk.StringVar(value="")
        self.tamil_char_label = tk.Label(char_display_frame, textvariable=self.tamil_char_var,
                                        font=(self.tamil_font, 120), bg="#1c2e3c", fg="#ecf0f1",
                                        height=1)
        self.tamil_char_label.pack(pady=5)
        
        # Pronunciation with better formatting
        pronunciation_frame = tk.Frame(self.results_frame, bg="#34495e")
        pronunciation_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(pronunciation_frame, text="Pronunciation:", 
                font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
        self.pronunciation_var = tk.StringVar(value="No detection yet")
        self.pronunciation_label = tk.Label(pronunciation_frame, textvariable=self.pronunciation_var, 
                                          font=("Arial", 12), bg="#34495e", fg="white")
        self.pronunciation_label.pack(side=tk.LEFT, padx=5)
        
        # Confidence with progress bar
        confidence_frame = tk.Frame(self.results_frame, bg="#34495e")
        confidence_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(confidence_frame, text="Confidence:", 
                font=("Arial", 12, "bold"), bg="#34495e", fg="#f39c12").pack(side=tk.LEFT, padx=5)
        
        self.confidence_var = tk.StringVar(value="0.00%")
        self.confidence_label = tk.Label(confidence_frame, textvariable=self.confidence_var, 
                                        font=("Arial", 12), bg="#34495e", fg="white")
        self.confidence_label.pack(side=tk.LEFT, padx=5)
        
        # Add a progress bar for confidence
        self.confidence_progress_frame = tk.Frame(self.results_frame, bg="#34495e", height=25)
        self.confidence_progress_frame.pack(fill=tk.X, pady=5)
        
        self.confidence_progress = tk.Canvas(self.confidence_progress_frame, 
                                            bg="#2c3e50", height=25, bd=0, highlightthickness=0)
        self.confidence_progress.pack(fill=tk.X)
    
    def update_threshold_label(self, event=None):
        """Update the threshold value label"""
        self.threshold_value_label.config(text=f"{self.confidence_threshold.get():.1f}")
        
    def browse_model(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Keras Model", "*.keras"), 
            ("H5 Model", "*.h5"),
            ("All Files", "*.*")
        ])
        if file_path:
            self.model_path_var.set(file_path)
            
    def browse_labels(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("JSON Files", "*.json"),
            ("All Files", "*.*")
        ])
        if file_path:
            self.labels_path_var.set(file_path)
            
    def load_model_and_labels(self):
        model_path = self.model_path_var.get()
        labels_path = self.labels_path_var.get()
        
        if not model_path:
            messagebox.showerror("Error", "Please select a model file")
            return
            
        if not labels_path:
            messagebox.showerror("Error", "Please select a labels file")
            return
            
        if not os.path.exists(model_path):
            messagebox.showerror("Error", f"Model file not found: {model_path}")
            return
            
        if not os.path.exists(labels_path):
            messagebox.showerror("Error", f"Labels file not found: {labels_path}")
            return
            
        try:
            self.status_var.set("Status: Loading model and labels...")
            self.root.update()
            
            # Load the model
            self.model = load_model(model_path)
            
            # Load the Tamil labels
            with open(labels_path, 'r', encoding='utf-8') as f:
                self.tamil_labels = json.load(f)
            
            # Convert string keys to integers
            self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
            
            self.model_loaded = True
            
            # Enable buttons
            self.image_btn.config(state=tk.NORMAL)
            self.webcam_btn.config(state=tk.NORMAL)
            
            # Update status
            self.status_var.set("Status: Model and labels loaded successfully")
            messagebox.showinfo("Success", "Model and labels loaded successfully")
            
            # Create reference grid
            self.create_reference_grid()
            
        except Exception as e:
            self.status_var.set(f"Status: Error loading model or labels")
            messagebox.showerror("Error", f"Failed to load: {str(e)}")
            
    def create_reference_grid(self):
        """Create a scrollable grid of reference Tamil characters"""
        # Clear existing content
        self.reference_canvas.delete("all")
        
        # Create a frame inside the canvas to hold the characters
        frame = tk.Frame(self.reference_canvas, bg="#2c3e50")
        self.reference_canvas.create_window((0, 0), window=frame, anchor="nw")
        
        # Add characters in a grid (10 per row)
        row, col = 0, 0
        self.reference_labels = {}  # Store references to labels for highlighting
        
        for char_id in sorted(self.tamil_labels.keys()):
            if char_id == 247:  # Skip background class (if applicable)
                continue
                
            # Create frame for each character
            char_frame = tk.Frame(frame, bg="#34495e", width=60, height=60, 
                                 padx=2, pady=2, borderwidth=1, relief=tk.RAISED)
            char_frame.grid(row=row, column=col, padx=3, pady=3)
            char_frame.grid_propagate(False)  # Keep fixed size
            
            # Add Tamil character with improved font
            char_label = tk.Label(char_frame, text=self.tamil_labels[char_id]["tamil"], 
                                 font=(self.tamil_font, 16), bg="#34495e", fg="white")
            char_label.pack(expand=True)
            
            # Store reference to this label
            self.reference_labels[self.tamil_labels[char_id]["tamil"]] = char_label
            
            # Tooltip with pronunciation
            self.create_tooltip(char_label, f"{self.tamil_labels[char_id]['tamil']} - {self.tamil_labels[char_id]['pronunciation']}")
            
            # Update row and column
            col += 1
            if col >= 8:  # Reduce columns to fit better
                col = 0
                row += 1
        
        # Update the canvas scroll region
        frame.update_idletasks()
        self.reference_canvas.config(scrollregion=self.reference_canvas.bbox("all"))
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.reference_canvas, orient=tk.HORIZONTAL, 
                                command=self.reference_canvas.xview)
        self.reference_canvas.config(xscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def enter(event):
            # Create a new tooltip window when mouse enters
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)  # Remove window decorations
            
            # Create label inside the tooltip window
            label = tk.Label(tooltip, text=text, bg="yellow", relief=tk.SOLID, borderwidth=1)
            label.pack()
            
            # Position the tooltip near the widget
            x, y, _, _ = widget.bbox("all") if hasattr(widget, 'bbox') else (0, 0, 0, 0)
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip.wm_geometry(f"+{x}+{y}")
            
            # Store the tooltip reference on the widget
            widget.tooltip = tooltip
            
        def leave(event):
            # Destroy the tooltip when mouse leaves
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
            
        # Bind events
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def process_image(self):
        if not self.model_loaded:
            messagebox.showerror("Error", "Please load the model and labels first")
            return
            
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
            ("All Files", "*.*")
        ])
        
        if not file_path:
            return
            
        try:
            # Read image with proper error handling
            image = self.read_image_safely(file_path)
            
            if image is None:
                messagebox.showerror("Error", f"Failed to read image: {file_path}")
                return
                
            # Update status while processing
            self.status_var.set(f"Status: Processing image {os.path.basename(file_path)}...")
            self.root.update()
            
            # Extract keypoints and make prediction
            result_image, tamil_char, pronunciation, confidence = self.analyze_image(image)
            
            # Save a copy of the processed image for debugging (optional)
            debug_path = f"debug_{os.path.basename(file_path)}"
            cv2.imwrite(debug_path, result_image)
            
            # Update display - make sure image is shown
            self.display_image(result_image)
            self.update_results(tamil_char, pronunciation, confidence)
            self.status_var.set(f"Status: Processed image {os.path.basename(file_path)}")
            
            # Add to history
            self.add_to_history(tamil_char, pronunciation, confidence)
            
        except Exception as e:
            self.status_var.set("Status: Error processing image")
            error_msg = f"Failed to process image: {str(e)}"
            print(error_msg)  # Print to console for debugging
            messagebox.showerror("Error", error_msg)
    
    def read_image_safely(self, file_path):
        """Read an image with multiple methods for better reliability"""
        # Try standard OpenCV reading
        image = cv2.imread(file_path)
        
        # If that fails, try with PIL and convert to OpenCV format
        if image is None:
            try:
                pil_image = Image.open(file_path)
                image = np.array(pil_image.convert('RGB'))
                # Convert from RGB to BGR format for OpenCV
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"PIL image loading failed too: {str(e)}")
                return None
                
        return image
                
    def toggle_webcam(self):
        if not self.model_loaded:
            messagebox.showerror("Error", "Please load the model and labels first")
            return
            
        if self.is_webcam_active:
            # Stop webcam
            self.stop_thread = True
            if self.detection_thread:
                self.detection_thread.join(timeout=1.0)
            if self.cap and self.cap.isOpened():
                self.cap.release()
            self.is_webcam_active = False
            self.webcam_btn.config(text="Start Webcam", bg="#9b59b6")
            self.capture_btn.config(state=tk.DISABLED)
            self.status_var.set("Status: Webcam stopped")
        else:
            # Start webcam
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Failed to open webcam")
                return
                
            self.is_webcam_active = True
            self.webcam_btn.config(text="Stop Webcam", bg="#e74c3c")
            self.capture_btn.config(state=tk.NORMAL)
            self.status_var.set("Status: Webcam active")
            
            # Start detection thread
            self.stop_thread = False
            self.detection_thread = threading.Thread(target=self.webcam_detection_loop)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            
    def webcam_detection_loop(self):
        """Process webcam frames and detect Tamil finger spellings"""
        prev_char = None
        stability_count = 0
        
        while not self.stop_thread and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read from webcam")
                    break
                    
                # Flip the frame horizontally for a more natural view
                frame = cv2.flip(frame, 1)
                    
                # Extract keypoints and make prediction
                result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
                # Stability check (to reduce flickering)
                if tamil_char == prev_char:
                    stability_count += 1
                else:
                    stability_count = 0
                    
                # Only update the display if prediction is stable or very confident
                if stability_count >= 3 or confidence > 80:
                    # Use a lambda with no parameters to ensure thread-safety
                    self.root.after(0, lambda f=result_frame: self.display_image(f))
                    self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
                                    self.update_results(t, p, c))
                    
                    # If prediction changes with high confidence, add to history
                    if tamil_char != prev_char and tamil_char and confidence > 65:
                        self.root.after(0, lambda t=tamil_char, p=pronunciation, c=confidence: 
                                        self.add_to_history(t, p, c))
                        
                    prev_char = tamil_char
                else:
                    # Just update the display without updating results
                    self.root.after(0, lambda f=result_frame: self.display_image(f))
                
                # If we're in word practice mode, check for character recognition
                if self.word_practice_active and tamil_char:
                    self.check_word_practice_progress(tamil_char, confidence)
                
                # Small delay to reduce CPU usage and make UI more responsive
                time.sleep(0.03)  # Approximate 30 FPS
                
            except Exception as e:
                print(f"Error in webcam loop: {str(e)}")
                time.sleep(0.1)
            
    def capture_frame(self):
        if not self.is_webcam_active or not self.cap:
            return
            
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame")
            return
            
        # Flip the frame horizontally for a more natural view
        frame = cv2.flip(frame, 1)
        
        # Save the captured frame
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"capture_{timestamp}.jpg"
        cv2.imwrite(save_path, frame)
        
        # Process the captured frame
        result_image, tamil_char, pronunciation, confidence = self.analyze_image(frame)
        
        # Update results
        self.update_results(tamil_char, pronunciation, confidence)
        self.add_to_history(tamil_char, pronunciation, confidence)
        
        # Display notification
        self.status_var.set(f"Status: Captured frame saved as {save_path}")
        messagebox.showinfo("Capture", f"Frame captured and saved as {save_path}")
            
    def analyze_image(self, image):
        """Analyze image and return the recognized Tamil character"""
        # Extract hand keypoints
        keypoints, annotated_image, hands_detected = self.extract_hand_keypoints(image)
        if not hands_detected:
            return annotated_image, "", "No hands detected", 0.0
            
        # Predict gesture
        predicted_class, confidence = self.predict_gesture(keypoints)
        
        # Get Tamil character and pronunciation
        if predicted_class in self.tamil_labels:
            tamil_char = self.tamil_labels[predicted_class]["tamil"]
            pronunciation = self.tamil_labels[predicted_class]["pronunciation"]
        else:
            tamil_char = "?"
            pronunciation = f"Unknown class: {predicted_class}"
        
        # Add prediction text to image
        cv2.putText(annotated_image, pronunciation, (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(annotated_image, f"Confidence: {confidence:.2f}%", (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        
        return annotated_image, tamil_char, pronunciation, confidence
            
    def extract_hand_keypoints(self, image):
        """Extract hand keypoints using MediaPipe"""
        # Convert to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image with MediaPipe
        results = self.hands.process(image_rgb)
        
        # Initialize placeholders for hand keypoints
        left_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        right_hand = np.zeros(21 * 2)  # 42 features (21 landmarks × x, y)
        
        # Make a copy of the image for drawing
        annotated_image = image.copy()
        
        # Extract keypoints if hands are detected
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_keypoints = []
                for landmark in hand_landmarks.landmark:
                    hand_keypoints.append(landmark.x)
                    hand_keypoints.append(landmark.y)
                
                # Assign to left or right hand (simplified for demonstration)
                if hand_idx == 0:
                    left_hand = hand_keypoints
                elif hand_idx == 1:
                    right_hand = hand_keypoints
                
                # Draw landmarks on the image
                self.mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        # Concatenate left & right hand keypoints
        data_aux = np.concatenate([left_hand, right_hand])
        
        return data_aux, annotated_image, results.multi_hand_landmarks is not None
        
    def predict_gesture(self, keypoints):
        """Predict the Tamil character gesture"""
        # Reshape input for LSTM: (samples=1, time steps=1, features=84)
        input_data = keypoints.reshape(1, 1, 84)
        
        # Make prediction with the model
        prediction = self.model.predict(input_data, verbose=0)
        
        # Get the class with highest probability
        predicted_class = np.argmax(prediction)
        confidence = np.max(prediction) * 100
        
        return predicted_class, confidence
            
    def display_image(self, image):
        """Display image on canvas with proper scaling"""
        try:
            # Convert OpenCV BGR image to RGB for Tkinter
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # If canvas hasn't been fully initialized yet, use default values
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = 640  # Default width
                canvas_height = 480  # Default height
            
            # Calculate scaling factor to fit canvas while maintaining aspect ratio
            img_height, img_width = image_rgb.shape[:2]
            scale = min(canvas_width/img_width, canvas_height/img_height)
            
            # New dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image
            if scale != 1.0:  # Only resize if needed
                image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
                                      interpolation=cv2.INTER_AREA)
            
            # Convert to PhotoImage
            image_pil = Image.fromarray(image_rgb)
            image_tk = ImageTk.PhotoImage(image=image_pil)
            
            # Clear previous content and update canvas
            self.canvas.delete("all")
            
            # Center the image on the canvas
            x_offset = max(0, (canvas_width - new_width) // 2)
            y_offset = max(0, (canvas_height - new_height) // 2)
            
            # Draw a border around the image area
            self.canvas.create_rectangle(
                x_offset-2, y_offset-2, 
                x_offset+new_width+2, y_offset+new_height+2,
                outline="#3498db", width=2
            )
            
            # Create image
            self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
            self.canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
            # Force update to ensure image is displayed
            self.canvas.update()
            
        except Exception as e:
            print(f"Error displaying image: {str(e)}")
        
    def update_results(self, tamil_char, pronunciation, confidence):
        """Update the results display with enhanced visuals"""
        self.tamil_char_var.set(tamil_char)
        self.pronunciation_var.set(pronunciation)
        self.confidence_var.set(f"{confidence:.2f}%")
        self.update_confidence_progress(confidence)
        
        # Highlight the detected character in the reference grid
        self.highlight_reference_character(tamil_char)
    def update_confidence_progress(self, confidence):
        """Update the confidence progress bar"""
        self.confidence_progress.delete("all")
        width = self.confidence_progress.winfo_width()
        if width < 10:  # Not yet properly initialized
            width = 200
        
        # Draw the background
        self.confidence_progress.create_rectangle(0, 0, width, 25, fill="#2c3e50", outline="")
        
        # Draw the progress bar
        progress_width = int(width * confidence / 100)
        
        # Color based on confidence level
        if confidence < 30:
            color = "#e74c3c"  # Red for low confidence
        elif confidence < 70:
            color = "#f39c12"  # Orange for medium confidence
        else:
            color = "#2ecc71"  # Green for high confidence
        
        self.confidence_progress.create_rectangle(0, 0, progress_width, 25, 
                                                 fill=color, outline="")
        
        # Add text
        self.confidence_progress.create_text(width/2, 13, 
                                            text=f"{confidence:.2f}%", 
                                            fill="white", font=("Arial", 12, "bold"))
    
    def highlight_reference_character(self, tamil_char):
        """Highlight the detected character in the reference grid"""
        # Reset all characters to normal background
        for label in self.reference_labels.values():
            label.config(bg="#34495e")
        
        # Highlight the detected character if it exists in our reference grid
        if tamil_char in self.reference_labels:
            self.reference_labels[tamil_char].config(bg="#e74c3c")  # Highlight with a red background
        
    def add_to_history(self, tamil_char, pronunciation, confidence):
        """Add detection to history"""
        if not tamil_char:  # Skip empty detections
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {tamil_char} ({pronunciation}) - {confidence:.2f}%\n"
        
        # Enable text widget for editing
        self.history_text.config(state=tk.NORMAL)
        
        # Insert at the beginning
        self.history_text.insert("1.0", history_entry)
        
        # Limit history length
        if float(self.history_text.index('end-1c').split('.')[0]) > 20:
            self.history_text.delete("20.0", tk.END)
            
        # Disable editing
        self.history_text.config(state=tk.DISABLED)
        
    def clear_history(self):
        """Clear detection history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    # ---------------------- GUESSING GAME FUNCTIONS ----------------------
    
    def start_guessing_game(self):
        """Initialize and start the character guessing game"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create the game UI
        self.create_guessing_game_ui()
        
        # Load model and labels if not already loaded
        if not self.model_loaded:
            model_path = self.default_model_path if os.path.exists(self.default_model_path) else ""
            labels_path = self.default_labels_path if os.path.exists(self.default_labels_path) else ""
            
            if model_path and labels_path:
                try:
                    # Load the model
                    self.model = load_model(model_path)
                    
                    # Load the Tamil labels
                    with open(labels_path, 'r', encoding='utf-8') as f:
                        self.tamil_labels = json.load(f)
                    
                    # Convert string keys to integers
                    self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
                    
                    self.model_loaded = True
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load model or labels: {str(e)}")
                    self.show_main_menu()
                    return
            else:
                messagebox.showerror("Error", "Model or labels file not found. Please load them manually.")
                self.show_main_menu()
                return
                
        # Check for reference images folder
        if not os.path.exists("ReferenceImages"):
            messagebox.showerror("Error", "ReferenceImages folder not found!")
            self.show_main_menu()
            return
            
        # Start webcam
        self.start_game_webcam()
        
        # Select first character for guessing
        self.select_random_character()
    
    def create_guessing_game_ui(self):
        """Create the UI for the guessing game"""
        game_frame = tk.Frame(self.root, bg="#2c3e50")
        game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top section with title and navigation
        top_frame = tk.Frame(game_frame, bg="#34495e", padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        # Title
        tk.Label(top_frame, text="Tamil Character Guessing Game", 
                font=("Arial", 20, "bold"), bg="#34495e", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_btn = tk.Button(top_frame, text="Main Menu", command=self.end_game_and_return,
                            bg="#e74c3c", fg="white", font=("Arial", 12), padx=15, pady=5)
        back_btn.pack(side=tk.RIGHT, padx=10)
        
        # Middle section with game content
        content_frame = tk.Frame(game_frame, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Split content into left and right parts
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left side - Reference image and score
        left_frame = tk.Frame(content_frame, bg="#34495e", padx=20, pady=20)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Game instructions
        instructions_label = tk.Label(left_frame, 
                                    text="What Tamil character does this hand sign represent?", 
                                    font=("Arial", 14), bg="#34495e", fg="white", 
                                    wraplength=400, justify=tk.LEFT)
        instructions_label.pack(pady=(0, 20))
        
        # Frame for reference image
        ref_image_frame = tk.Frame(left_frame, bg="#2c3e50", padx=5, pady=5)
        ref_image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Reference image label
        self.ref_image_label = tk.Label(ref_image_frame, bg="#1c2e3c")
        self.ref_image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Score section
        score_frame = tk.LabelFrame(left_frame, text="Score", 
                                  font=("Arial", 14, "bold"), bg="#34495e", fg="white", 
                                  padx=15, pady=15)
        score_frame.pack(fill=tk.X, pady=10)
        
        score_display = tk.Frame(score_frame, bg="#34495e")
        score_display.pack(fill=tk.X)
        
        # Current score
        self.score_var = tk.StringVar(value="0")
        tk.Label(score_display, text="Points:", 
                font=("Arial", 16, "bold"), bg="#34495e", fg="#2ecc71").grid(row=0, column=0, padx=10)
        tk.Label(score_display, textvariable=self.score_var, 
                font=("Arial", 24, "bold"), bg="#34495e", fg="#2ecc71").grid(row=0, column=1, padx=10)
        
        # Total attempts
        self.attempts_var = tk.StringVar(value="0")
        tk.Label(score_display, text="Attempts:", 
                font=("Arial", 16), bg="#34495e", fg="white").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(score_display, textvariable=self.attempts_var, 
                font=("Arial", 16), bg="#34495e", fg="white").grid(row=1, column=1, padx=10, pady=5)
        
        # Next character button
        next_btn = tk.Button(left_frame, text="Skip / Next Hand Sign", 
                           command=self.select_random_character,
                           bg="#3498db", fg="white", font=("Arial", 14), padx=10, pady=5)
        next_btn.pack(fill=tk.X, pady=10)
        
        # Right side - Character selection
        right_frame = tk.Frame(content_frame, bg="#34495e", padx=20, pady=20)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Title for character selection
        selection_title = tk.Label(right_frame, text="Select the Correct Character", 
                                 font=("Arial", 16, "bold"), bg="#34495e", fg="white")
        selection_title.pack(pady=(0, 20))
        
        # Character selection grid
        self.char_selection_frame = tk.Frame(right_frame, bg="#34495e")
        self.char_selection_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame for feedback
        feedback_frame = tk.Frame(right_frame, bg="#34495e", height=100)
        feedback_frame.pack(fill=tk.X, pady=10)
        
        # Feedback message
        self.feedback_var = tk.StringVar(value="Choose the character that matches the hand sign")
        self.feedback_label = tk.Label(feedback_frame, textvariable=self.feedback_var, 
                                     font=("Arial", 14), bg="#34495e", fg="#f39c12", 
                                     wraplength=400, pady=10)
        self.feedback_label.pack(fill=tk.X, pady=10)
        
        # Answer reveal section
        self.answer_frame = tk.Frame(right_frame, bg="#34495e", padx=10, pady=10)
        self.answer_frame.pack(fill=tk.X)
        
        self.answer_var = tk.StringVar(value="")
        self.answer_label = tk.Label(self.answer_frame, textvariable=self.answer_var,
                                    font=("Arial", 16), bg="#34495e", fg="#2ecc71")
        self.answer_label.pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Game ready! Select the character matching the hand sign.")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                  font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_guessing_game(self):
        """Initialize and start the character guessing game"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create the game UI
        self.create_guessing_game_ui()
        
        # Load model and labels if not already loaded
        if not self.model_loaded:
            labels_path = self.default_labels_path if os.path.exists(self.default_labels_path) else ""
            
            if labels_path:
                try:
                    # Load the Tamil labels
                    with open(labels_path, 'r', encoding='utf-8') as f:
                        self.tamil_labels = json.load(f)
                    
                    # Convert string keys to integers
                    self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
                    
                    self.model_loaded = True
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load labels: {str(e)}")
                    self.show_main_menu()
                    return
            else:
                messagebox.showerror("Error", "Labels file not found. Please load them manually.")
                self.show_main_menu()
                return
                
        # Check for reference images folder
        if not os.path.exists("ReferenceImages"):
            messagebox.showerror("Error", "ReferenceImages folder not found!")
            self.show_main_menu()
            return
        
        # Create character selection grid
        self.create_character_selection_grid()
            
        # Select first character for guessing
        self.select_random_character()
    
    def create_character_selection_grid(self):
        """Create a grid of Tamil characters for selection"""
        # Clear existing grid
        for widget in self.char_selection_frame.winfo_children():
            widget.destroy()
        
        # Create a scrollable frame
        canvas = tk.Canvas(self.char_selection_frame, bg="#34495e")
        scrollbar = tk.Scrollbar(self.char_selection_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Get unique Tamil characters for selection
        unique_chars = []
        for char_id, info in self.tamil_labels.items():
            tamil_char = info["tamil"]
            if tamil_char not in unique_chars:
                unique_chars.append(tamil_char)
        
        # Create a grid layout for characters
        row, col = 0, 0
        max_cols = 4  # Number of columns in the grid
        
        for char in unique_chars:
            # Get pronunciation for this character
            pronunciation = ""
            for info in self.tamil_labels.values():
                if info["tamil"] == char:
                    pronunciation = info["pronunciation"]
                    break
            
            # Create a button for each character
            button_frame = tk.Frame(scrollable_frame, bg="#2c3e50", padx=5, pady=5)
            button_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # Character button
            char_button = tk.Button(
                button_frame,
                text=char,
                font=(self.tamil_font, 24),
                width=3,
                height=2,
                bg="#3498db",
                fg="white",
                command=lambda c=char, p=pronunciation: self.check_character_guess(c, p)
            )
            char_button.pack(pady=2)
            
            # Pronunciation label
            tk.Label(button_frame, text=pronunciation, font=("Arial", 10), bg="#2c3e50", fg="white").pack()
            
            # Update row and column
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def select_random_character(self):
        """Select a random Tamil character for the guessing game"""
        try:
            # Get all files in ReferenceImages folder
            image_files = [f for f in os.listdir("ReferenceImages") 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            
            if not image_files:
                messagebox.showerror("Error", "No image files found in ReferenceImages folder!")
                return
                
            # Select a random image
            random_file = random.choice(image_files)
            file_path = os.path.join("ReferenceImages", random_file)
            
            # Parse the image filename to get index and pronunciation
            parts = os.path.splitext(random_file)[0].split('_')
            if len(parts) >= 2:
                index = int(parts[0])
                pronunciation = parts[1]
                
                # Find the corresponding Tamil character
                tamil_char = ""
                for char_id, info in self.tamil_labels.items():
                    if info["pronunciation"].lower() == pronunciation.lower():
                        tamil_char = info["tamil"]
                        break
                
                # Load and display the image
                try:
                    img = Image.open(file_path)
                    img = img.resize((350, 350), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    
                    self.ref_image_label.config(image=img_tk)
                    self.ref_image_label.image = img_tk  # Keep a reference
                    
                    # Store the correct answer
                    self.current_guessing_answer = tamil_char
                    self.current_guessing_image = random_file
                    
                    # Reset feedback and answer display
                    self.feedback_var.set("Choose the character that matches the hand sign")
                    self.answer_var.set("")
                    
                    # Enable all character buttons
                    for widget in self.char_selection_frame.winfo_children():
                        widget.configure(state=tk.NORMAL)
                    
                except Exception as e:
                    print(f"Error loading image {file_path}: {str(e)}")
                    messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            else:
                messagebox.showerror("Error", f"Invalid image filename format: {random_file}")
                
        except Exception as e:
            print(f"Error selecting random character: {str(e)}")
            messagebox.showerror("Error", f"Failed to select random character: {str(e)}")
    
    def check_character_guess(self, selected_char, pronunciation):
        """Check if the selected character matches the current guessing answer"""
        # Increment attempts
        self.total_attempts += 1
        self.attempts_var.set(str(self.total_attempts))
        
        # Check if the selected character matches the correct answer
        if selected_char == self.current_guessing_answer:
            # Correct guess
            self.current_score += 1
            self.score_var.set(str(self.current_score))
            
            # Show success message
            self.feedback_var.set("Excellent! You selected the correct character!")
            self.answer_var.set(f"Correct: {self.current_guessing_answer} ({pronunciation})")
            self.status_var.set(f"Correct! +1 point. Total: {self.current_score}")
            
            # Schedule next character after a delay
            self.root.after(2000, self.select_random_character)
        else:
            # Incorrect guess
            self.feedback_var.set("Sorry, that's not the correct character. Try again!")
            
            # Show the correct pronunciation
            correct_pronunciation = ""
            for info in self.tamil_labels.values():
                if info["tamil"] == self.current_guessing_answer:
                    correct_pronunciation = info["pronunciation"]
                    break
                    
            self.answer_var.set(f"The correct answer is: {self.current_guessing_answer} ({correct_pronunciation})")
    
    def end_game_and_return(self):
        """End the game and return to main menu"""
        # Return to main menu
        self.show_main_menu()
        
    def select_random_character(self):
        """Select a random Tamil character for the guessing game"""
        try:
            # Get all files in ReferenceImages folder
            image_files = [f for f in os.listdir("ReferenceImages") 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            
            if not image_files:
                messagebox.showerror("Error", "No image files found in ReferenceImages folder!")
                return
                
            # Select a random image
            random_file = random.choice(image_files)
            file_path = os.path.join("ReferenceImages", random_file)
            
            # Parse the image filename to get index and pronunciation
            parts = os.path.splitext(random_file)[0].split('_')
            if len(parts) >= 2:
                index = int(parts[0])
                pronunciation = parts[1]
                
                # Find the corresponding Tamil character
                tamil_char = ""
                for char_id, info in self.tamil_labels.items():
                    if info["pronunciation"].lower() == pronunciation.lower():
                        tamil_char = info["tamil"]
                        break
                
                # Load and display the image
                try:
                    img = Image.open(file_path)
                    img = img.resize((350, 350), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    
                    self.ref_image_label.config(image=img_tk)
                    self.ref_image_label.image = img_tk  # Keep a reference
                    
                    # Store the correct answer
                    self.current_guessing_answer = tamil_char
                    self.current_guessing_image = random_file
                    
                    # Make sure we only access UI elements that exist in this mode
                    if hasattr(self, 'target_char_var'):
                        self.target_char_var.set(tamil_char)
                    
                    if hasattr(self, 'target_pronun_var'):
                        self.target_pronun_var.set(pronunciation)
                    
                    if hasattr(self, 'feedback_var'):
                        self.feedback_var.set("Choose the character that matches the hand sign")
                    
                    if hasattr(self, 'answer_var'):
                        self.answer_var.set("")
                    
                    # Enable all character buttons if they exist
                    if hasattr(self, 'char_selection_frame'):
                        for widget in self.char_selection_frame.winfo_children():
                            if isinstance(widget, tk.Button):
                                widget.configure(state=tk.NORMAL)
                    
                except Exception as e:
                    print(f"Error loading image {file_path}: {str(e)}")
                    messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            else:
                messagebox.showerror("Error", f"Invalid image filename format: {random_file}")
                
        except Exception as e:
            print(f"Error selecting random character: {str(e)}")
            messagebox.showerror("Error", f"Failed to select random character: {str(e)}")
    
    def display_game_image(self, image):
        """Display image on game canvas"""
        try:
            # Convert OpenCV BGR image to RGB for Tkinter
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get canvas dimensions
            canvas_width = self.game_canvas.winfo_width()
            canvas_height = self.game_canvas.winfo_height()
            
            # If canvas hasn't been fully initialized yet, use default values
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = 640  # Default width
                canvas_height = 360  # Default height
            
            # Calculate scaling factor to fit canvas while maintaining aspect ratio
            img_height, img_width = image_rgb.shape[:2]
            scale = min(canvas_width/img_width, canvas_height/img_height)
            
            # New dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image
            if scale != 1.0:  # Only resize if needed
                image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
                                      interpolation=cv2.INTER_AREA)
            
            # Convert to PhotoImage
            image_pil = Image.fromarray(image_rgb)
            image_tk = ImageTk.PhotoImage(image=image_pil)
            
            # Clear previous content and update canvas
            self.game_canvas.delete("all")
            
            # Center the image on the canvas
            x_offset = max(0, (canvas_width - new_width) // 2)
            y_offset = max(0, (canvas_height - new_height) // 2)
            
            # Create image
            self.game_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
            self.game_canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
        except Exception as e:
            print(f"Error displaying game image: {str(e)}")
    
    def update_game_detection(self, tamil_char, pronunciation):
        """Update the detected character display in the game"""
        self.detected_char_var.set(tamil_char)
        self.detected_pronun_var.set(pronunciation)
    
    def update_feedback(self, message):
        """Update feedback message in the game"""
        self.feedback_var.set(message)
    
    def award_point(self):
        """Award a point for correct guessing and move to next character"""
        # Increment score
        self.current_score += 1
        self.score_var.set(str(self.current_score))
        
        # Increment attempts
        self.total_attempts += 1
        self.attempts_var.set(str(self.total_attempts))
        
        # Show success message
        self.feedback_var.set("Excellent! You got it right!")
        self.status_var.set(f"Correct! +1 point. Total: {self.current_score}")
        
        # Schedule next character after a delay
        self.root.after(1500, self.select_random_character)
    
    # ---------------------- WORD PRACTICE FUNCTIONS ----------------------
    
    def start_word_practice(self):
        """Initialize and start the word practice mode"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create the word practice UI
        self.create_word_practice_ui()
        
        # Load model and labels if not already loaded
        if not self.model_loaded:
            model_path = self.default_model_path if os.path.exists(self.default_model_path) else ""
            labels_path = self.default_labels_path if os.path.exists(self.default_labels_path) else ""
            
            if model_path and labels_path:
                try:
                    # Load the model
                    self.model = load_model(model_path)
                    
                    # Load the Tamil labels
                    with open(labels_path, 'r', encoding='utf-8') as f:
                        self.tamil_labels = json.load(f)
                    
                    # Convert string keys to integers
                    self.tamil_labels = {int(k): v for k, v in self.tamil_labels.items()}
                    
                    self.model_loaded = True
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load model or labels: {str(e)}")
                    self.show_main_menu()
                    return
            else:
                messagebox.showerror("Error", "Model or labels file not found. Please load them manually.")
                self.show_main_menu()
                return
        
        # Start webcam
        self.start_word_practice_webcam()
        
        # Display initial word selection
        self.show_word_selection()
    def create_word_practice_ui(self):
        """Create the UI for word practice mode"""
        practice_frame = tk.Frame(self.root, bg="#2c3e50")
        practice_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top section with title and navigation
        top_frame = tk.Frame(practice_frame, bg="#34495e", padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        # Title
        tk.Label(top_frame, text="Tamil Word Practice", 
                font=("Arial", 20, "bold"), bg="#34495e", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_btn = tk.Button(top_frame, text="Main Menu", command=self.end_practice_and_return,
                            bg="#e74c3c", fg="white", font=("Arial", 12), padx=15, pady=5)
        back_btn.pack(side=tk.RIGHT, padx=10)
        
        # Main content layout
        content_frame = tk.Frame(practice_frame, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Split content into left and right parts with adjusted weights to make left side larger
        content_frame.columnconfigure(0, weight=3)  # Left side gets more space
        content_frame.columnconfigure(1, weight=2)  # Right side gets less space
        content_frame.rowconfigure(0, weight=1)
        
        # Left side - Word selection, LARGE reference image, and progress
        left_frame = tk.Frame(content_frame, bg="#34495e", padx=20, pady=20)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Set up grid layout for left frame
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=0)  # Word selection - fixed height
        left_frame.rowconfigure(1, weight=0)  # Progress tracking - fixed height
        left_frame.rowconfigure(2, weight=5)  # Reference image - gets most space
        left_frame.rowconfigure(3, weight=0)  # Current character info - fixed height
        left_frame.rowconfigure(4, weight=0)  # Instructions - fixed height
        
        # Word selection - Row 0
        word_select_frame = tk.LabelFrame(left_frame, text="Word Selection", 
                                        font=("Arial", 14, "bold"), bg="#34495e", fg="white", 
                                        padx=15, pady=10)
        word_select_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Current word display
        self.practice_word_var = tk.StringVar(value="Select a word to practice")
        self.practice_word_label = tk.Label(word_select_frame, textvariable=self.practice_word_var, 
                                        font=("Arial", 18, "bold"), bg="#34495e", fg="#f39c12")
        self.practice_word_label.pack(pady=5)
        
        # Word buttons
        self.word_buttons_frame = tk.Frame(word_select_frame, bg="#34495e")
        self.word_buttons_frame.pack(fill=tk.X, pady=5)
        
        # Progress section - Row 1
        progress_frame = tk.LabelFrame(left_frame, text="Progress", 
                                    font=("Arial", 14, "bold"), bg="#34495e", fg="white", 
                                    padx=15, pady=10)
        progress_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Character sequence display
        self.char_sequence_frame = tk.Frame(progress_frame, bg="#34495e")
        self.char_sequence_frame.pack(fill=tk.X, pady=5)
        
        # MAXIMUM SIZE Reference image frame - Row 2 (main section)
        ref_frame = tk.LabelFrame(left_frame, text="Reference Hand Sign", 
                                font=("Arial", 18, "bold"), bg="#34495e", fg="white",
                                padx=25, pady=25)
        # Make this frame take up most space
        ref_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Reference image display - MAXIMUM SIZE
        # Create a container frame with fixed minimum size to ensure large images
        ref_img_container = tk.Frame(ref_frame, bg="#1c2e3c", width=1000, height=1000)
        ref_img_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ref_img_container.pack_propagate(False)  # Prevent container from shrinking
        
        self.practice_ref_image_label = tk.Label(ref_img_container, bg="#1c2e3c")
        self.practice_ref_image_label.pack(fill=tk.BOTH, expand=True)
        
        # Current character info - Row 3 (now shows pronunciation only)
        current_char_frame = tk.LabelFrame(left_frame, text="Current Hand Sign", 
                                        font=("Arial", 12, "bold"), bg="#34495e", fg="white")
        current_char_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        # Pronunciation of current character (larger and more prominent)
        self.current_pronun_var = tk.StringVar(value="")
        self.current_pronun_label = tk.Label(current_char_frame, textvariable=self.current_pronun_var, 
                                        font=("Arial", 24, "bold"), bg="#34495e", fg="white")
        self.current_pronun_label.pack(pady=10)
        
        # Instruction label - Row 4
        self.instruction_var = tk.StringVar(value="Select a word to begin practice")
        self.instruction_label = tk.Label(left_frame, textvariable=self.instruction_var, 
                                        font=("Arial", 14), bg="#34495e", fg="#3498db", 
                                        wraplength=400)
        self.instruction_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        
        # Right side - Webcam and detection
        right_frame = tk.Frame(content_frame, bg="#34495e", padx=20, pady=20)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Webcam view
        camera_label = tk.Label(right_frame, text="Camera View", 
                            font=("Arial", 14, "bold"), bg="#34495e", fg="white")
        camera_label.pack(pady=(0, 10))
        
        self.practice_canvas = tk.Canvas(right_frame, bg="black", width=640, height=360)
        self.practice_canvas.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Detected character display
        detect_frame = tk.LabelFrame(right_frame, text="Your Sign", 
                                    font=("Arial", 14, "bold"), bg="#34495e", fg="white", 
                                    padx=15, pady=15)
        detect_frame.pack(fill=tk.X, pady=10)
        
        # Character display
        self.practice_detected_char_var = tk.StringVar(value="")
        self.practice_detected_char_label = tk.Label(detect_frame, textvariable=self.practice_detected_char_var, 
                                                font=(self.tamil_font, 60), bg="#1c2e3c", fg="#ecf0f1", 
                                                width=3, height=1)
        self.practice_detected_char_label.pack(pady=10)
        
        # Pronunciation
        detect_pronun_frame = tk.Frame(detect_frame, bg="#34495e")
        detect_pronun_frame.pack(fill=tk.X, pady=5)
        
        self.practice_detected_pronun_var = tk.StringVar(value="Make a hand sign")
        self.practice_detected_pronun_label = tk.Label(detect_pronun_frame, 
                                                    textvariable=self.practice_detected_pronun_var, 
                                                    font=("Arial", 14), bg="#34495e", fg="white")
        self.practice_detected_pronun_label.pack(pady=5)
        
        # Feedback message
        self.practice_feedback_var = tk.StringVar(value="Copy the hand sign shown on the left")
        self.practice_feedback_label = tk.Label(right_frame, textvariable=self.practice_feedback_var, 
                                            font=("Arial", 14), bg="#34495e", fg="#f39c12", 
                                            wraplength=400)
        self.practice_feedback_label.pack(fill=tk.X, pady=10)
        
        # Skip button (for difficult gestures)
        self.skip_btn = tk.Button(right_frame, text="Skip This Hand Sign", 
                            command=self.skip_current_character,
                            bg="#7f8c8d", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.skip_btn.pack(pady=10)
        self.skip_btn.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to practice Tamil words")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1", 
                                bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_practice_word(self, word, char_indices):
        """Select a word for practice and set up the sequence"""
        self.current_practice_word = word
        self.current_word_chars = []
        
        # Reset UI
        self.practice_word_var.set(f"Practicing: {word}")
        self.instruction_var.set("Copy the hand signs shown to form this word")
        
        # Clear sequence display
        for widget in self.char_sequence_frame.winfo_children():
            widget.destroy()
            
        # Create character sequence display
        self.char_boxes = []
        
        for i, char_id in enumerate(char_indices):
            if char_id in self.tamil_labels:
                char_info = self.tamil_labels[char_id]
                tamil_char = char_info["tamil"]
                pronunciation = char_info["pronunciation"]
                
                # Find reference image with correct naming format: [CharID]_[Pronunciation].jpg
                image_path = self.find_reference_image_for_char_id(char_id)
                
                # Create a mini frame for this character in the sequence
                char_frame = tk.Frame(self.char_sequence_frame, bg="#34495e", padx=5, pady=5)
                char_frame.pack(side=tk.LEFT)
                
                # Load a mini version of the hand gesture image if available
                mini_image_label = None
                if image_path and os.path.exists(image_path):
                    try:
                        mini_img = Image.open(image_path)
                        mini_img = mini_img.resize((60, 60), Image.LANCZOS)
                        mini_img_tk = ImageTk.PhotoImage(mini_img)
                        
                        mini_image_label = tk.Label(char_frame, image=mini_img_tk, 
                                                bg="#34495e", bd=2, relief=tk.SUNKEN)
                        mini_image_label.image = mini_img_tk  # Keep reference
                        mini_image_label.pack(pady=2)
                    except Exception as e:
                        print(f"Error creating mini image: {str(e)}")
                        mini_image_label = None
                
                # If no image available, use Tamil character as fallback
                if mini_image_label is None:
                    char_label = tk.Label(char_frame, text=tamil_char, 
                                        font=(self.tamil_font, 24), bg="#34495e", fg="#bdc3c7",
                                        width=2, height=1)
                    char_label.pack(pady=2)
                else:
                    char_label = mini_image_label
                
                # Pronunciation label
                pronun_label = tk.Label(char_frame, text=pronunciation, 
                                    font=("Arial", 10), bg="#34495e", fg="#bdc3c7")
                pronun_label.pack()
                
                # Store character info
                self.current_word_chars.append({
                    "id": char_id,
                    "tamil": tamil_char,
                    "pronunciation": pronunciation,
                    "frame": char_frame,
                    "char_label": char_label,
                    "pronun_label": pronun_label,
                    "completed": False,
                    "image_path": image_path
                })
        
        # Start practice with first character
        self.current_char_index = 0
        self.word_practice_active = True
        self.update_current_practice_char()
        
        # Enable the skip button
        self.skip_btn.config(state=tk.NORMAL)
        
        # Start webcam if not already active
        if not self.is_webcam_active:
            self.start_word_practice_webcam()

    def update_current_practice_char(self):
        """Update the current character to be practiced - focusing on hand gesture"""
        try:
            if self.current_char_index < len(self.current_word_chars):
                current = self.current_word_chars[self.current_char_index]
                
                # Update sequence highlighting
                for i, char_info in enumerate(self.current_word_chars):
                    if i < self.current_char_index:
                        # Completed characters
                        char_info["pronun_label"].config(bg="#27ae60", fg="white")
                        char_info["frame"].config(bg="#27ae60")
                        if hasattr(char_info["char_label"], "config"):
                            char_info["char_label"].config(bg="#27ae60", fg="white")
                    elif i == self.current_char_index:
                        # Current character
                        char_info["pronun_label"].config(bg="#f39c12", fg="white")
                        char_info["frame"].config(bg="#f39c12")
                        if hasattr(char_info["char_label"], "config"):
                            char_info["char_label"].config(bg="#f39c12", fg="white")
                    else:
                        # Upcoming characters
                        char_info["pronun_label"].config(bg="#34495e", fg="#bdc3c7")
                        char_info["frame"].config(bg="#34495e")
                        if hasattr(char_info["char_label"], "config"):
                            char_info["char_label"].config(bg="#34495e", fg="#bdc3c7")
                
                # Update the pronunciation display (now the main identifier)
                self.current_pronun_var.set(current["pronunciation"])
                
                # Display the reference image for this character - LARGE HAND GESTURE IMAGE
                if "image_path" in current and current["image_path"] and os.path.exists(current["image_path"]):
                    try:
                        print(f"Loading reference image from: {current['image_path']}")
                        img = Image.open(current["image_path"])
                        
                        # FIX: Set an even larger fixed size for the hand sign image
                        # This ensures it's always clearly visible regardless of the container size
                        fixed_size = (1000, 1000)
                        
                        # FIX: Use appropriate resampling filter based on PIL/Pillow version
                        try:
                            # For newer Pillow versions
                            img = img.resize(fixed_size, Image.Resampling.LANCZOS)
                        except AttributeError:
                            try:
                                # For older Pillow versions
                                img = img.resize(fixed_size, Image.LANCZOS)
                            except AttributeError:
                                # Fallback to ANTIALIAS for very old versions
                                img = img.resize(fixed_size, Image.ANTIALIAS)
                        
                        img_tk = ImageTk.PhotoImage(img)
                        
                        # Show the image 
                        self.practice_ref_image_label.config(image=img_tk)
                        self.practice_ref_image_label.image = img_tk  # Keep a reference
                        
                        # Update instruction
                        self.instruction_var.set(f"Copy this hand sign for '{current['pronunciation']}'")
                        self.practice_feedback_var.set("Show your hand to the camera and make the same sign")
                        
                    except Exception as e:
                        print(f"Error displaying reference image: {str(e)}")
                        self.practice_ref_image_label.config(image='')
                        self.instruction_var.set(f"Error displaying hand sign image. Try to make the sign for '{current['pronunciation']}'")
                else:
                    self.practice_ref_image_label.config(image='')
                    if "image_path" in current:
                        print(f"Image not found: {current.get('image_path', 'No path specified')}")
                    self.instruction_var.set(f"No reference image available. Try to make the sign for '{current['pronunciation']}'")
                    
            else:
                # Word completed
                self.word_practice_active = False
                
                # Update UI to show completion
                self.current_pronun_var.set("Word completed!")
                self.instruction_var.set("Well done! You've completed all the signs for this word. Choose another word to practice.")
                self.practice_feedback_var.set("Congratulations! Word completed successfully.")
                
                # Clear the reference image
                self.practice_ref_image_label.config(image='')
                
                # Show congratulatory message
                self.status_var.set(f"Congratulations! You completed the word '{self.current_practice_word}'")
                
                # Disable skip button
                self.skip_btn.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error in update_current_practice_char: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def word_practice_webcam_loop(self):
        """Process webcam frames for word practice"""
        prev_char = None
        stability_count = 0
        
        while not self.stop_thread and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read from webcam")
                    break
                    
                # Flip the frame horizontally for a more natural view
                frame = cv2.flip(frame, 1)
                    
                # Extract keypoints and make prediction
                result_frame, tamil_char, pronunciation, confidence = self.analyze_image(frame)
                
                # Stability check (to reduce flickering)
                if tamil_char == prev_char:
                    stability_count += 1
                else:
                    stability_count = 0
                    
                # Only update the display if prediction is stable or very confident
                if stability_count >= 2 or confidence > 75:
                    # Update detected character display
                    self.root.after(0, lambda t=tamil_char, p=pronunciation: 
                                self.update_practice_detection(t, p))
                    
                    # Check if word practice is active and we have a current character
                    if self.word_practice_active and self.current_char_index < len(self.current_word_chars):
                        current = self.current_word_chars[self.current_char_index]
                        
                        # Check if detected character matches the current target
                        if tamil_char == current["tamil"] and confidence > 70:
                            # Mark this character as completed and move to next immediately
                            current["completed"] = True
                            self.current_char_index += 1
                            
                            # Give positive feedback
                            self.root.after(0, lambda: 
                                        self.practice_feedback_var.set("Correct! Moving to next sign..."))
                            
                            # Update to next character or complete word
                            self.root.after(500, self.update_current_practice_char)
                
                # Add word practice info to the frame
                if self.word_practice_active and self.current_char_index < len(self.current_word_chars):
                    current = self.current_word_chars[self.current_char_index]
                    cv2.putText(result_frame, f"Make sign: {current['pronunciation']}", 
                            (10, result_frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, (255, 255, 0), 2)
                
                # Update the display
                self.root.after(0, lambda f=result_frame: self.display_practice_image(f))
                
                prev_char = tamil_char
                
                # Small delay to reduce CPU usage
                time.sleep(0.03)
                
            except Exception as e:
                print(f"Error in word practice webcam loop: {str(e)}")
                time.sleep(0.1)

    def find_reference_image_for_char_id(self, char_id):
        """Find the reference image path for a given character ID
        
        Format: [CharID]_[Pronunciation].jpg
        Example: 1_a.jpg where 1 is the index and a is the pronunciation
        """
        try:
            # Check if the character exists in our mapping
            if char_id in self.tamil_labels:
                char_info = self.tamil_labels[char_id]
                pronunciation = char_info.get("pronunciation", "")
                
                # Build the expected filename
                filename = f"{char_id}_{pronunciation}.jpg"
                
                # Check in the ReferenceImages directory
                image_path = os.path.join("ReferenceImages", filename)
                print(f"Looking for image: {image_path}")
                
                # Verify the file exists
                if os.path.exists(image_path):
                    print(f"Found reference image: {image_path}")
                    return image_path
                
                # Try alternative image extensions if jpg doesn't exist
                for ext in ['.png', '.jpeg', '.gif']:
                    alt_path = os.path.join("ReferenceImages", f"{char_id}_{pronunciation}{ext}")
                    if os.path.exists(alt_path):
                        print(f"Found reference image with alternative extension: {alt_path}")
                        return alt_path
                
                print(f"Warning: No reference image found for character ID {char_id} ({pronunciation})")
                return None
            else:
                print(f"Warning: Character ID {char_id} not found in label mapping")
                return None
        except Exception as e:
            print(f"Error finding reference image: {str(e)}")
            return None

    def update_practice_detection(self, tamil_char, pronunciation):
        """Update the detected character display in word practice"""
        self.practice_detected_char_var.set(tamil_char)
        self.practice_detected_pronun_var.set(pronunciation if pronunciation else "No detection")

    def skip_current_character(self):
        """Skip the current character and move to the next one"""
        if self.word_practice_active and self.current_char_index < len(self.current_word_chars):
            # Mark as skipped rather than completed
            self.current_word_chars[self.current_char_index]["completed"] = True
            self.current_char_index += 1
            self.char_recognized_time = 0
            
            # Update to next character
            self.update_current_practice_char()
            self.status_var.set(f"Skipped to next hand sign")

    def display_practice_image(self, image):
        """Display image on practice canvas"""
        try:
            # Convert OpenCV BGR image to RGB for Tkinter
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get canvas dimensions
            canvas_width = self.practice_canvas.winfo_width()
            canvas_height = self.practice_canvas.winfo_height()
            
            # If canvas hasn't been fully initialized yet, use default values
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = 640  # Default width
                canvas_height = 360  # Default height
            
            # Calculate scaling factor to fit canvas while maintaining aspect ratio
            img_height, img_width = image_rgb.shape[:2]
            scale = min(canvas_width/img_width, canvas_height/img_height)
            
            # New dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image
            if scale != 1.0:  # Only resize if needed
                image_rgb = cv2.resize(image_rgb, (new_width, new_height), 
                                    interpolation=cv2.INTER_AREA)
            
            # Convert to PhotoImage
            image_pil = Image.fromarray(image_rgb)
            image_tk = ImageTk.PhotoImage(image=image_pil)
            
            # Clear previous content and update canvas
            self.practice_canvas.delete("all")
            
            # Center the image on the canvas
            x_offset = max(0, (canvas_width - new_width) // 2)
            y_offset = max(0, (canvas_height - new_height) // 2)
            
            # Create image
            self.practice_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image_tk)
            self.practice_canvas.image = image_tk  # Keep a reference to prevent garbage collection
            
        except Exception as e:
            print(f"Error displaying practice image: {str(e)}")

    def show_word_selection(self):
        """Show word selection buttons"""
        # Clear existing buttons
        for widget in self.word_buttons_frame.winfo_children():
            widget.destroy()
            
        # Add a button for each word
        for i, (word, char_indices) in enumerate(COMMON_WORDS.items()):
            btn = tk.Button(self.word_buttons_frame, text=word, 
                        command=lambda w=word, c=char_indices: self.select_practice_word(w, c),
                        bg="#3498db", fg="white", font=("Arial", 12), 
                        padx=15, pady=5, width=25)
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            
        # Make columns equal width
        self.word_buttons_frame.columnconfigure(0, weight=1)

    def start_word_practice_webcam(self):
        """Start webcam for word practice"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open webcam")
            self.show_main_menu()
            return
            
        self.is_webcam_active = True
        self.status_var.set("Status: Webcam active. Select a word to practice.")
        
        # Start detection thread
        self.stop_thread = False
        self.detection_thread = threading.Thread(target=self.word_practice_webcam_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
    def end_practice_and_return(self):
        """End word practice and return to main menu"""
        # Stop webcam if active
        self.stop_thread = True
        if self.detection_thread:
            self.detection_thread.join(timeout=1.0)
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.is_webcam_active = False
        self.word_practice_active = False
        
        # Return to main menu
        self.show_main_menu()
    
    def cleanup(self):
        """Clean up resources before closing"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.stop_thread = True
        if self.detection_thread:
            self.detection_thread.join(timeout=1.0)
        print("Application closed, resources released")

def create_tamil_label_mapping():
    """Create the Tamil character label mapping"""
    # Check if labels file already exists
    if os.path.exists("tamil_labels.json"):
        print("Tamil labels file already exists.")
        return
    
    # If we needed to create a default Tamil labels file,
    # we would add that code here. For now, we'll assume
    # the file is provided by the user.
    print("Tamil labels file not found. Please provide a valid labels file.")

def main():
    # Ensure label mapping file exists
    create_tamil_label_mapping()
    
    # Create and run the GUI
    root = tk.Tk()
    app = TamilFingerSpellingGUI(root)
    
    # Set up cleanup on exit
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()