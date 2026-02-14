import os
import sys
import subprocess
import shutil
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class TelegramManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Telegarm Manager")
        self.geometry("400x550")
        self.resizable(False, False)

        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.bin_dir = os.path.join(self.base_dir, "bin")
        self.exe_path = os.path.join(self.bin_dir, "Telegram.exe")
        self.profiles_dir = os.path.join(self.base_dir, "profiles")

        # Create dirs
        if not os.path.exists(self.profiles_dir): os.makedirs(self.profiles_dir)
        if not os.path.exists(self.bin_dir): os.makedirs(self.bin_dir)

        # Layout
        self.create_widgets()
        self.refresh_profiles()

    def create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="TeleManager", 
                                      font=("Roboto Medium", 20))
        self.title_label.pack(pady=15)

        # Scrollable Area for Accounts
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Your Accounts")
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Footer / Add Button
        self.btn_add = ctk.CTkButton(self, text="+ Create New Profile", 
                                   command=self.add_profile, height=40,
                                   font=("Roboto Medium", 14))
        self.btn_add.pack(fill="x", padx=15, pady=15)

    def check_exe(self):
        if not os.path.exists(self.exe_path):
            messagebox.showerror("Error", f"Telegram.exe not found!\n\nPlease put 'Telegram.exe' inside:\n{self.bin_dir}")
            return False
        return True

    def launch_telegram(self, account_name):
        if not self.check_exe(): return

        profile_path = os.path.join(self.profiles_dir, account_name)
        if not os.path.exists(profile_path): os.makedirs(profile_path)
        
        # Launch independently
        subprocess.Popen([self.exe_path, "-workdir", profile_path])

    def add_profile(self):
        dialog = ctk.CTkInputDialog(text="Enter Profile Name (e.g. Work):", title="New Profile")
        name = dialog.get_input()
        if name:
            safe_name = "".join(x for x in name if x.isalnum() or x in "._- ")
            self.launch_telegram(safe_name)
            self.refresh_profiles()

    def delete_profile(self, name):
        if messagebox.askyesno("Delete", f"Are you sure you want to delete '{name}'?\nThis will remove all login data for this account."):
            path = os.path.join(self.profiles_dir, name)
            try:
                shutil.rmtree(path)
                self.refresh_profiles()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_profiles(self):
        # Clear list
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Scan folder
        if os.path.exists(self.profiles_dir):
            accounts = [f for f in os.listdir(self.profiles_dir) if os.path.isdir(os.path.join(self.profiles_dir, f))]
            
            if not accounts:
                ctk.CTkLabel(self.scroll_frame, text="No profiles found.").pack(pady=20)

            for acc in accounts:
                row = ctk.CTkFrame(self.scroll_frame)
                row.pack(fill="x", pady=5)
                
                # Account Name
                lbl = ctk.CTkLabel(row, text=acc, font=("Roboto", 14), anchor="w")
                lbl.pack(side="left", padx=10, pady=10)
                
                # Delete Button (Small X)
                del_btn = ctk.CTkButton(row, text="X", width=30, fg_color="#cf3a3a", hover_color="#8a1c1c",
                                      command=lambda a=acc: self.delete_profile(a))
                del_btn.pack(side="right", padx=5)

                # Open Button
                open_btn = ctk.CTkButton(row, text="Open", width=80, 
                                       command=lambda a=acc: self.launch_telegram(a))
                open_btn.pack(side="right", padx=5)

if __name__ == "__main__":
    app = TelegramManagerApp()
    app.mainloop()