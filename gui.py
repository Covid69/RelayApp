import tkinter as tk
from relay_app import RelayApp
import serial.tools.list_ports
import re
import warnings


class USBRelayManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("USB Relay Manager")
        self.geometry("300x300")
        self.option_add('*font', 'Arial 10')
        self.port_list = []
        self.find_com_port()
        self.interface = None

        # Device Selection
        self.device_label = tk.Label(self, text="Select Device:")
        self.device_label.pack()
        self.device_var = tk.StringVar()
        # Display default value for port select dropdown list
        self.device_var.set(self.port_list[-1])
        self.device_menu = tk.OptionMenu(self, self.device_var, *self.port_list)
        self.device_menu.pack()
    

        # Open/Close Device Buttons
        device_control_frame = tk.Frame(self)
        device_control_frame.pack(pady=20)
        self.open_device_button = tk.Button(device_control_frame, text="Open Device", command=self.open_device)
        self.open_device_button.pack(side=tk.LEFT)
        self.close_device_button = tk.Button(device_control_frame, text="Close Device", command=self.close_device)
        self.close_device_button.pack(side=tk.LEFT)

        # Relay Controls
        self.relays = []
        for i in range(2):
            relay_frame = tk.Frame(self)
            relay_frame.pack()

            # Relay Label
            relay_label = tk.Label(relay_frame, text=f"Relay {i}")
            relay_label.pack(side=tk.LEFT)

            # Open/Close Buttons
            open_button = tk.Button(relay_frame, text="Open", fg="green", command=lambda i=i: self.open_relay(i))
            open_button.pack(side=tk.LEFT)
            close_button = tk.Button(relay_frame, text="Close", fg="red", command=lambda i=i: self.close_relay(i))
            close_button.pack(side=tk.LEFT)
            # Status Label
            self.relay_status_label = tk.Label(relay_frame, text="Unknown", fg="black")  # Initial status as Unknown
            self.relay_status_label.pack(side=tk.LEFT)

            # Store references to buttons and label for each relay
            self.relays.append((open_button, close_button, self.relay_status_label))

        # Control All Buttons
        control_all_frame = tk.Frame(self)
        control_all_frame.pack(side=tk.BOTTOM, pady=10)  # Add padding below the frame
        self.open_all_button = tk.Button(control_all_frame, text="Open All", fg="green", command=self.open_all)
        self.open_all_button.pack(side=tk.LEFT)
        self.close_all_button = tk.Button(control_all_frame, text="Close All", fg="red", command=self.close_all)
        self.close_all_button.pack(side=tk.LEFT)
        self.ComLabel = tk.Label(self, text="Not Opened")
        self.ComLabel.pack(side=tk.BOTTOM, pady=10)


    # Placeholder functions for relay control (update status labels)
    def open_device(self):
        # Implement logic to update relay statuses after opening device
        print("Opening device...")
        if self.interface != None:
            warnings.warn(f"Another COM port has already been opened. Close it first")
        else:
            try:
                self.interface = RelayApp(self.device_var.get())
            finally:
                if self.interface == None:
                    warnings.warn(f"Failed to open COM: {self.device_var.get()}")
                else:
                    self.update_relay_stat()
                    print(f"{self.device_var.get()} opened successfully")
                    self.ComLabel.config(text=f"{self.device_var.get()} Opened", fg="green")
      
    def close_device(self):
        # Implement logic to update relay statuses after closing device
        print("Closing device...")
        if self.interface == None:
            warnings.warn(f"No port has been opened")
            self.ComLabel.config(text=f"No port has been opened", fg="red")
        else:
            self.relays[0][2].config(text="Unknown", fg="black")
            self.relays[1][2].config(text="Unknown", fg="black") 
            try:
                print(f"{self.interface.port} closed successfully")
                self.ComLabel.config(text=f"{self.interface.port} Closed", fg="red")
            finally:
                self.interface = None
  

    def open_relay(self, relay_index):
        if self.interface == None:
            warnings.warn(f"No port has been opened")
            self.ComLabel.config(text=f"No port has been opened", fg="red")
        else:
            print(f"Opening relay {relay_index}")
            # Implement logic to send open command and update status label (e.g., "Open")
            # print(self.interface.current_status)
            mask = 1 << relay_index
            intValue = int(self.interface.current_status) | mask
            sendData = str(intValue).encode()
            print(sendData)
            self.interface.serial_write(bytes(sendData))
            self.update_relay_stat()

    def close_relay(self, relay_index):
        if self.interface == None:
            warnings.warn(f"No port has been opened")
            self.ComLabel.config(text=f"No port has been opened", fg="red")
        else:
            print(f"Closing relay {relay_index}")
            mask = ~(1 << relay_index)
            intValue = int(self.interface.current_status) & mask
            sendData = str(intValue).encode()
            print(sendData)
            self.interface.serial_write(bytes(sendData))
            self.update_relay_stat()

    def find_com_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port,Description,port1 in sorted(ports):
            print("{}".format(port))
            self.port_list.append(port)

    def open_all(self):
        if self.interface == None:
            warnings.warn(f"No port has been opened")
            self.ComLabel.config(text=f"No port has been opened", fg="red")
        else:
            print(f"Opening all relays")
            self.interface.serial_write(b'3')
            self.update_relay_stat()

    def close_all(self):
        if self.interface == None:
            warnings.warn(f"No port has been opened")
            self.ComLabel.config(text=f"No port has been opened", fg="red")
        else:
            print(f"Opening all relays")
            self.interface.serial_write(b'0')
            self.update_relay_stat()
    
    def update_relay_stat(self):
        self.interface.current_status = self.interface.read_state()
        if self.interface.current_status == b'0':
            self.relays[0][2].config(text="Closed", fg="red")
            self.relays[1][2].config(text="Closed", fg="red")
        elif self.interface.current_status == b'1':
            self.relays[0][2].config(text="Open", fg="green")
            self.relays[1][2].config(text="Closed", fg="red")
        elif self.interface.current_status == b'2':
            self.relays[0][2].config(text="Closed", fg="red")
            self.relays[1][2].config(text="Open", fg="green")
        elif self.interface.current_status == b'3':
            self.relays[0][2].config(text="Open", fg="green")
            self.relays[1][2].config(text="Open", fg="green")

if __name__ == "__main__":
  app = USBRelayManager()
  app.mainloop()