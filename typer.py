

from functools import reduce
from tkinter import *
from tkinter import filedialog
import time
from tkinter import messagebox
import copy


root = Tk()
start_time = 61
id_timer = None
typed_text = []
all_text =[]
root.option_add('*Font', 'Arial 16')




    
# Метод для получения текста из внешнего файла 
def extract_text():
    file_name = filedialog.askopenfile()
    global all_text
    if file_name:
        file_name_entry.insert(0, str(file_name.name))
        text = file_name.read()
        fill_text(text)


# Метод для заполнения поля с текстом 
def fill_text(text):
        global all_text
        text = text.split()
        all_text = copy.copy(text)
        text_with_text.delete('1.0', END)
        text_with_text.insert('1.0', text)
    
    
# Событие нажатия кнопки клавиатуры на поле
def key_pressed(event):
    print(str(event))
    if event.keycode == 32:
        new_word = enter_field.get().strip()
        typed_text.append(new_word)
        enter_field.delete(0, END)
        text_with_text.delete('1.0', END)
        for index, word in enumerate(typed_text):
            if word == all_text[index]:
                text_with_text.insert(END, all_text[index] + ' ', 'green')
            else:
                text_with_text.insert(END, all_text[index] + ' ', 'red')
        for word in all_text[len(typed_text):]:
            text_with_text.insert(END, word + ' ')
            
            
# Обновление таймера каждую секунду, если время выйдет или количество введенных слов 
# совпадет с количеством в тексте, то произойдет вызов функции с всплывающим окном
def update_timer():
    global start_time
    global id_timer
    global typed_text
    start_time -= 1
    time_label.config(text=str(start_time))
    if start_time == 0 or len(typed_text) == len(all_text):
        time_label.after_cancel(id_timer)
        start_button.config(state=NORMAL)
        end_of_typing(61 - start_time)
        typed_text = []
    else:
        id_timer = time_label.after(1000, update_timer)

# Начало отсчета таймера при нажатии на кнопку
def start_timer():
    global start_time
    start_time = 61
    update_timer()
    global typed_text
    typed_text = []
    start_button.config(state=DISABLED)


# Вывод всплывающего окна
def end_of_typing(time_spent):
    result = {}
    typed_text_len = len(all_text)
    all_text_len = len(all_text)

    for i in all_text:
        result[i] = typed_text.count(i)

    typed_text_len = reduce(lambda x, y: x + y, result.values(), 0)

    messagebox.showinfo("Конец",f"Ваш результат: {typed_text_len} слов из {all_text_len}, это {round(typed_text_len * (61/time_spent), 1)} слов в минуту!")

frame_for_file = Frame(master=root, width=300, height=300, bg='gray')
frame_for_text = Frame(master=root, width=100, height=20, bg='gray')
frame_for_enter = Frame(master=root, width=400,height=20, bg='gray')

accept_button = Button(text='Выбрать файл', master=frame_for_file, command=extract_text)
accept_button.pack(side=LEFT, padx=10, pady=5)

file_name_entry = Entry(master=frame_for_file, width=40)
file_name_entry.pack(side=LEFT, padx=10, pady=5)

text_with_text = Text(master=frame_for_text, width=50, height=8)
text_with_text.tag_config('green', foreground='green')
text_with_text.tag_config('red', foreground='red')
text_with_text.tag_config('black', foreground='black')

text_with_text.pack()

#
fill_text("The quick brown fox jumps over the lazy dog")


enter_field = Entry(master=frame_for_enter, width=40, background='white')
enter_field.bind('<Key>', key_pressed)
enter_field.pack(side=LEFT, padx=10, pady=5)


start_button = Button(text='Старт', master=frame_for_enter, command=start_timer)
start_button.pack(side=LEFT, padx=10, pady=5)

time_label = Label(master=frame_for_enter, text='00')
time_label.pack(side=LEFT)

frame_for_file.pack(fill=BOTH)
frame_for_text.pack(expand=True, fill=BOTH)
frame_for_enter.pack(fill=BOTH)
root.mainloop()
