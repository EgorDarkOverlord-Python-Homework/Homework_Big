from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import Image, ImageTk  # pip install pillow
import cv2
import numpy as np
from image_processing import *

loaded_image = None
zoom = 1

NOISE_IMAGE = "Зашумление"
DENOISE_IMAGE = "Удаление шума"
EQUALIZATION = "Эквивализация"
STATISTIC_CORRECTION = "Статистическая цветокоррекция"
SCALE = "Масштабирование"
TRANSLATION = "Перенос"
ROTATION = "Поворот"
GLASS_EFFECT = "Эффект стекла"
MOTION_BLUR = "Motion Blur"


def set_image_to_label(label, image, zoom=1):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(
        image.resize((int(image.width * zoom), int(image.height * zoom)))
    )
    label.configure(image=image)
    label.image = image


def resize_image(scale):
    try:
        global zoom
        zoom *= scale
        set_image_to_label(image_label, loaded_image, zoom)
    except cv2.error as e:
        if e.err == "!_src.empty()":
            showerror("Ошибка", "Изображение не загружено")


def on_load_image_button_click():
    path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=(
            ("jpeg files", "*.jpg"),
            ("png files", "*.png"),
            ("all files", "*.*"),
        ),
    )

    try:
        global loaded_image
        loaded_image = cv2.imdecode(
            np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED
        )
        global zoom
        zoom = 1
        set_image_to_label(image_label, loaded_image, zoom)
    except Exception as e:
        showerror("Ошибка", "Некорректный путь")


def on_do_image_button_click():
    global loaded_image
    if loaded_image is None:
        showerror("Ошибка", "Изображение не загружено")
        return
    
    selection = augmentation_algorithm_combo.get()
    try:
        if selection == NOISE_IMAGE:
            percent = int(noise_entry.get())
            noise_image(loaded_image, percent)
        elif selection == DENOISE_IMAGE:
            power = int(denoise_entry.get())
            loaded_image = noise_filtering(loaded_image, power) 
        elif selection == EQUALIZATION:
            loaded_image = image_equalization(loaded_image)
        elif selection == STATISTIC_CORRECTION:
            loaded_image = statistic_correction(loaded_image)
        elif selection == SCALE:
            width = int(scale_w_entry.get())
            height = int(scale_h_entry.get())
            loaded_image = image_resize(loaded_image, width, height)
        elif selection == TRANSLATION:
            x = int(translation_x_entry.get())
            y = int(translation_y_entry.get())
            loaded_image = translation(loaded_image, x, y)
        elif selection == ROTATION:
            angle = int(rotation_entry.get())
            loaded_image = rotation(loaded_image, angle)
        elif selection == GLASS_EFFECT:
            power = int(glass_effect_entry.get())
            loaded_image = glass_effect(loaded_image, power)
        elif selection == MOTION_BLUR:
            power = int(motion_blur_power_entry.get())
            angle = int(motion_blur_angle_entry.get())
            loaded_image = motion_blur(loaded_image, power, angle)
        else:
            showerror("Ошибка", "Выберите способ обработки изображения")
    
        set_image_to_label(image_label, loaded_image, zoom)
    except ValueError as e:
        showerror("Ошибка", "Некорректно введённые данные")


def on_save_image_button_click():
    if loaded_image is None:
        showerror("Ошибка", "Изображение не загружено")
        return
    
    path = filedialog.asksaveasfilename(
        title="Сохранить файл",
        defaultextension="*.*",
        filetypes=(
            ("jpeg files", "*.jpg"),
            ("png files", "*.png"),            
        ),
    )

    try:
        format = f".{path.split('.')[-1]}"
        is_success, im_buf_arr = cv2.imencode(ext=format, img=loaded_image)
        im_buf_arr.tofile(path)
    except Exception as e:
        showerror("Ошибка", "Некорректный путь")


def on_augmentation_algorithm_combo_selected(event):
    noise_frame.grid_forget()
    denoise_frame.grid_forget()
    scale_frame.grid_forget()
    translation_frame.grid_forget()
    rotation_frame.grid_forget()
    glass_effect_frame.grid_forget()
    motion_blur_frame.grid_forget()

    selection = augmentation_algorithm_combo.get()

    if selection == NOISE_IMAGE:
        noise_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    elif selection == DENOISE_IMAGE:
        denoise_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    elif selection == SCALE:
        scale_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    elif selection == TRANSLATION:
        translation_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    elif selection == ROTATION:
        rotation_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    elif selection == GLASS_EFFECT:
        glass_effect_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    elif selection == MOTION_BLUR:
        motion_blur_frame.grid(row=2, column=0, sticky=EW, padx=5, pady=5)

window = Tk()
window.minsize(800, 600)
window.title("Аугментация данных")

window.columnconfigure(0, weight=1)

file_operations_frame = Frame(window)
file_operations_frame.grid(row=0, column=0, sticky=EW, padx=5, pady=5)

load_image_button = ttk.Button(
    file_operations_frame,
    text="Загрузить изображение",
    command=on_load_image_button_click,
)
load_image_button.pack(fill=X, side=LEFT, expand=True)
do_image_button = ttk.Button(
    file_operations_frame,
    text="Преобразовать изображение",
    command=on_do_image_button_click,
)
do_image_button.pack(fill=X, side=LEFT, expand=True)
save_image_button = ttk.Button(
    file_operations_frame, 
    text="Сохранить изображение",
    command=on_save_image_button_click,)
save_image_button.pack(fill=X, side=LEFT, expand=True)

base_settings_frame = Frame(window)
base_settings_frame.grid(row=1, column=0, sticky=EW, padx=5, pady=5)
augmentation_algorithm_label = ttk.Label(
    base_settings_frame, text="Алгоритм преобразования"
)
augmentation_algorithm_label.pack(side=LEFT)
augmentation_algorithm_combo = ttk.Combobox(
    base_settings_frame,
    values=[
        NOISE_IMAGE,
        DENOISE_IMAGE,
        EQUALIZATION,
        STATISTIC_CORRECTION,
        SCALE,
        TRANSLATION,
        ROTATION,
        GLASS_EFFECT,
        MOTION_BLUR
    ],
)
augmentation_algorithm_combo.bind("<<ComboboxSelected>>", on_augmentation_algorithm_combo_selected)
augmentation_algorithm_combo.pack(fill=X, side=LEFT, expand=True)

window.rowconfigure(3, weight=1)
canvas = Canvas(bg="white")
canvas.grid(row=3, column=0, sticky=NSEW, padx=5, pady=5)
image_label = Label(canvas)
image_label.place(relx=0.5, rely=0.5, anchor="center")

zoom_frame = Frame(window)
zoom_frame.grid(row=4, column=0, sticky=EW, padx=5, pady=5)
zoom_plus_button = ttk.Button(
    zoom_frame,
    text="+",
    command=lambda: resize_image(1.5),
)
zoom_plus_button.pack(side=LEFT)
zoom_minus_button = ttk.Button(
    zoom_frame,
    text="-",
    command=lambda: resize_image(1 / 1.5),
)
zoom_minus_button.pack(side=LEFT)

noise_frame = Frame(window)
noise_label = ttk.Label(
    noise_frame, text="Процент шумных пикселей"
)
noise_label.pack(side=LEFT)
noise_entry = ttk.Entry(noise_frame)
noise_entry.pack(fill=X, side=LEFT, expand=True)

denoise_frame = Frame(window)
denoise_label = ttk.Label(denoise_frame, text="Сила шумоподавления")
denoise_label.pack(side=LEFT)
denoise_entry = ttk.Entry(denoise_frame)
denoise_entry.pack(fill=X, side=LEFT, expand=True)

scale_frame = Frame(window)
scale_w_label = ttk.Label(scale_frame, text="Новая ширина")
scale_h_label = ttk.Label(scale_frame, text="Новая высота")
scale_w_entry = ttk.Entry(scale_frame)
scale_h_entry = ttk.Entry(scale_frame)
scale_frame.columnconfigure(1, weight=1)
scale_w_label.grid(row=0, column=0, sticky=W)
scale_w_entry.grid(row=0, column=1, sticky=EW)
scale_h_label.grid(row=1, column=0, sticky=W)
scale_h_entry.grid(row=1, column=1, sticky=EW)

translation_frame = Frame(window)
translation_x_label = ttk.Label(translation_frame, text="Перенос по X")
translation_y_label = ttk.Label(translation_frame, text="Перенос по Y")
translation_x_entry = ttk.Entry(translation_frame)
translation_y_entry = ttk.Entry(translation_frame)
translation_frame.columnconfigure(1, weight=1)
translation_x_label.grid(row=0, column=0, sticky=W)
translation_x_entry.grid(row=0, column=1, sticky=EW)
translation_y_label.grid(row=1, column=0, sticky=W)
translation_y_entry.grid(row=1, column=1, sticky=EW)

rotation_frame = Frame(window)
rotation_label = ttk.Label(rotation_frame, text="Угол поворота")
rotation_label.pack(side=LEFT)
rotation_entry = ttk.Entry(rotation_frame)
rotation_entry.pack(fill=X, side=LEFT, expand=True)

glass_effect_frame = Frame(window)
glass_effect_label = ttk.Label(glass_effect_frame, text="Сила эффекта")
glass_effect_label.pack(side=LEFT)
glass_effect_entry = ttk.Entry(glass_effect_frame)
glass_effect_entry.pack(fill=X, side=LEFT, expand=True)

motion_blur_frame = Frame(window)
motion_blur_power_label = ttk.Label(motion_blur_frame, text="Сила эффекта")
motion_blur_angle_label = ttk.Label(motion_blur_frame, text="Угол направления")
motion_blur_power_entry = ttk.Entry(motion_blur_frame)
motion_blur_angle_entry = ttk.Entry(motion_blur_frame)
motion_blur_frame.columnconfigure(1, weight=1)
motion_blur_power_label.grid(row=0, column=0, sticky=W)
motion_blur_power_entry.grid(row=0, column=1, sticky=EW)
motion_blur_angle_label.grid(row=1, column=0, sticky=W)
motion_blur_angle_entry.grid(row=1, column=1, sticky=EW)

window.mainloop()
