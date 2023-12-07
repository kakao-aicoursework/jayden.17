import json
import openai
import tkinter as tk
import pandas as pd
from tkinter import scrolledtext
import tkinter.filedialog as filedialog

openai.api_key = ''

# 저는 카카오 서비스 챗봇입니다.

def send_message(message_log, gpt_model="gpt-3.5-turbo", temperature=0.1):

    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=message_log,
        temperature=temperature
    )

    return response.choices[0].message.content


def main():

    def document():
        f = open("data/project_data_카카오소셜.txt", 'r')
        doc = []
        while True:
            line = f.readline()
            if not line:
                break
            doc.append(line)
        f.close()
        return doc


    message_log = [
        {
            "role": "system",
            "content": '''
                당신은 카카오 서비스 챗봇입니다. 다음의 서비스 설명을 참고해서 답변해주세요
                '''
        },
        {
            "role": "system",
            "content": f"{document()}"
        }
    ]


    def show_popup_message(window, message):
        popup = tk.Toplevel(window)
        popup.title("")

        # 팝업 창의 내용
        label = tk.Label(popup, text=message, font=("맑은 고딕", 12))
        label.pack(expand=True, fill=tk.BOTH)

        # 팝업 창의 크기 조절하기
        window.update_idletasks()
        popup_width = label.winfo_reqwidth() + 20
        popup_height = label.winfo_reqheight() + 20
        popup.geometry(f"{popup_width}x{popup_height}")

        # 팝업 창의 중앙에 위치하기
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f"+{popup_x}+{popup_y}")

        popup.transient(window)
        popup.attributes('-topmost', True)

        popup.update()
        return popup

    def on_send():
        user_input = user_entry.get()
        user_entry.delete(0, tk.END)

        if user_input.lower() == "quit":
            window.destroy()
            return

        message_log.append({"role": "user", "content": user_input})
        conversation.config(state=tk.NORMAL)  # 이동
        conversation.insert(tk.END, f"You: {user_input}\n", "user")  # 이동

        thinking_popup = show_popup_message(window, "처리중...")
        window.update_idletasks()

        response = send_message(message_log)
        thinking_popup.destroy()

        conversation.insert(tk.END, f"gpt assistant: {response}\n", "assistant")
        conversation.config(state=tk.DISABLED)
        conversation.see(tk.END)

    window = tk.Tk()
    window.title("GPT AI")

    font = ("맑은 고딕", 10)
    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, fg='black', bg='#f0f0f0', font=font)

    # width, height를 없애고 배경색 지정하기(2)
    conversation.tag_configure("user", background="#c9daf8")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.tag_configure("assistant", background="#e4e4e4")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # 창의 폭에 맞추어 크기 조정하기(4)

    input_frame = tk.Frame(window)  # user_entry와 send_button을 담는 frame(5)
    input_frame.pack(fill=tk.X, padx=10, pady=10)  # 창의 크기에 맞추어 조절하기(5)

    user_entry = tk.Entry(input_frame)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

    send_button = tk.Button(input_frame, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)

    window.bind('<Return>', lambda event: on_send())

    conversation.insert(tk.END, f"assistant: 저는 카카오 서비스 챗봇입니다.\n")

    window.mainloop()


if __name__ == "__main__":
    main()
