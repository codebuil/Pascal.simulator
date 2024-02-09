import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os



class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Barebone Builder")

        # Janela amarela
        self.root.configure(bg='yellow')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="Build", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="new file", command=self.copy_file)
        self.copy_button.pack(pady=5)

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):
        filename = tk.filedialog.askopenfilename(title="Select file")
        self.text_area.delete(1.0, tk.END)
        self.execute_command("mv -f kernel.bin /tmp/null",False)
        self.execute_command("mv -f /tmp/kernel.o /tmp/null",False)
        self.execute_command("mv -f /tmp/ppas.sh /tmp/null",False)
        self.execute_command("mv -f ppas.sh /tmp/null",False)
        self.execute_command("mv -f link.res /tmp/null",False)
        self.execute_command("unzip -u ./file/CD_root.zip -d /tmp",False)
        self.execute_command("as -o /tmp/boot.o ./file/boot.s",True)
        self.execute_command("nasm -o ./file/model.o ./file/model.asm",True)
        self.execute_command("gcc -c -nostdlib ./file/base.c  -o /tmp/base.o",True)

        fff=f'fpc -Cn -CcCDECL -O2 -Xs -Xs -Xt -Pi386 -Tlinux "$1"'.replace("$1",filename)
        
        self.execute_command(fff,True)
        self.execute_command("cp -f ppas.sh /tmp",False)
        self.execute_command("cp -f link.res /tmp",False)
        self.execute_command("mv -f ./kernel.o /tmp",False)
        self.execute_command("gcc -nostdlib -T ./file/link.ld /tmp/boot.o /tmp/base.o /tmp/kernel.o  -o /tmp/hello.elf",True)

        self.execute_command("cp -f /tmp/hello.elf /tmp/hello.c32",True)
        self.execute_command("dd if=/tmp/model.o of=/tmp/hello.elf  count=1 conv=notrunc",True)
        
        self.execute_command("cp -f /tmp/hello.elf /tmp/CD_root/isolinux/hello.c32",True)

        self.execute_command("genisoimage -o myos.iso -input-charset utf-8 -b isolinux/isolinux.bin -no-emul-boot -boot-load-size 4  -boot-info-table /tmp/CD_root ",True)
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        self.execute_command("qemu-system-x86_64 -serial msmouse -cdrom myos.iso",True)


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        filename = tk.filedialog.asksaveasfilename(title="Select file")
        if filename:
            shutil.copy( f"./file/new",filename+".c")
            self.text_area.insert(tk.END, f"File {filename} copied \n",True)


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
