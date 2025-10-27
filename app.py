import tkinter as tk
from tkinter import messagebox, simpledialog
import db

class MiniBankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('МахначБанк')
        self.resizable(False, False)
        self.current_user = None
        self._build_login()

    def _clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_login(self):
        self._clear_frame()
        frm = tk.Frame(self, padx=20, pady=20)
        frm.pack()

        tk.Label(frm, text='Логин:').grid(row=0, column=0, sticky='e')
        self.login_entry = tk.Entry(frm)
        self.login_entry.grid(row=0, column=1, pady=5)

        tk.Label(frm, text='Пин-код:').grid(row=1, column=0, sticky='e')
        self.pin_entry = tk.Entry(frm, show='*')
        self.pin_entry.grid(row=1, column=1, pady=5)

        login_btn = tk.Button(frm, text='Войти', width=15, command=self._attempt_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.login_entry.focus_set()

    def _attempt_login(self):
        login = self.login_entry.get().strip()
        pin_text = self.pin_entry.get().strip()
        if not login or not pin_text:
            messagebox.showwarning('Ошибка', 'Заполните логин и пин-код.')
            return
        try:
            pin = int(pin_text)
        except ValueError:
            messagebox.showwarning('Ошибка', 'Пин-код должен быть числом.')
            return

        user = db.get_user(login, pin)
        if user:
            self.current_user = user
            messagebox.showinfo('Успех', 'Успешный вход!')
            self._build_main_menu()
        else:
            messagebox.showerror('Ошибка', 'Неверный логин или пин-код.')

    def _build_main_menu(self):
        self._clear_frame()
        frm = tk.Frame(self, padx=20, pady=20)
        frm.pack()

        tk.Label(frm, text=f'Добро пожаловать, {self.current_user[1] if len(self.current_user)>1 else "клиент"}!', font=('TkDefaultFont', 12)).pack(pady=(0,10))

        btn_balance = tk.Button(frm, text='Просмотр баланса', width=25, command=self.show_balance)
        btn_deposit = tk.Button(frm, text='Пополнение счета', width=25, command=self.deposit)
        btn_withdraw = tk.Button(frm, text='Снятие средств', width=25, command=self.withdraw)
        btn_logout = tk.Button(frm, text='Выход из аккаунта', width=25, command=self.logout)
        btn_quit = tk.Button(frm, text='Закрыть приложение', width=25, command=self.destroy)

        btn_balance.pack(pady=5)
        btn_deposit.pack(pady=5)
        btn_withdraw.pack(pady=5)
        btn_logout.pack(pady=(15,5))
        btn_quit.pack(pady=5)

    def show_balance(self):
        user_id = self.current_user[0]
        balance = db.get_balance(user_id)
        messagebox.showinfo('Баланс', f'Ваш текущий баланс: {balance} гривен')

    def deposit(self):
        amount = simpledialog.askinteger('Пополнение', 'Введите сумму для пополнения:', minvalue=1, parent=self)
        if amount is None:
            return
        user_id = self.current_user[0]
        current = db.get_balance(user_id)
        new_balance = current + amount
        db.update_balance(user_id, new_balance)
        messagebox.showinfo('Успех', f'Счет пополнен на {amount} гривен.\nНовый баланс: {new_balance} гривен')

    def withdraw(self):
        amount = simpledialog.askinteger('Снятие', 'Введите сумму для снятия:', minvalue=1, parent=self)
        if amount is None:
            return
        user_id = self.current_user[0]
        current = db.get_balance(user_id)
        if amount <= current:
            new_balance = current - amount
            db.update_balance(user_id, new_balance)
            messagebox.showinfo('Успех', f'Вы сняли {amount} гривен.\nНовый баланс: {new_balance} гривен')
        else:
            messagebox.showerror('Ошибка', 'Недостаточно средств.')

    def logout(self):
        self.current_user = None
        messagebox.showinfo('Выход', 'Вы вышли из аккаунта.')
        self._build_login()

if __name__ == '__main__':
    app = MiniBankApp()
    app.mainloop()