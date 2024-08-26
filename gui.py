import tkinter as tk
from relay_app import RelayApp
import serial.tools.list_ports
import re
import warnings


class USBRelayManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("USB Relay Manager")
        self.geometry("300x200")
        self.port_list = []
        self.find_com_port()
        self.interface = None

        # Device Selection
        self.device_label = tk.Label(self, text="Select Device:")
        self.device_label.pack()
        self.device_var = tk.StringVar()
        # Display default value for port select dropdown list
        self.device_var.set(self.port_list[-1])
        # self.device_menu = tk.OptionMenu(self, self.device_var, *["Device 1", "Device 2", "Device 3"])
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
            open_button = tk.Button(relay_frame, text="Open", command=lambda i=i: self.open_relay(i))
            open_button.pack(side=tk.LEFT)
            close_button = tk.Button(relay_frame, text="Close", command=lambda i=i: self.close_relay(i))
            close_button.pack(side=tk.LEFT)
            # Status Label
            self.relay_status_label = tk.Label(relay_frame, text="Unknown")  # Initial status as Unknown
            self.relay_status_label.pack(side=tk.LEFT)

            # Store references to buttons and label for each relay
            self.relays.append((open_button, close_button, self.relay_status_label))

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
      
    def close_device(self):
        # Implement logic to update relay statuses after closing device
        print("Closing device...")
        if self.interface == None:
            warnings.warn(f"No port has been opened")
        else:
            self.relays[0][2].config(text="Unknown")
            self.relays[1][2].config(text="Unknown")
            print(f"{self.interface.port} closed successfully")
            self.interface = None
  

    def open_relay(self, relay_index):
        if self.interface == None:
            warnings.warn(f"No port has been opened")
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
        else:
            print(f"Closing relay {relay_index}")
            # Implement logic to send close command and update status label (e.g., "Closed")
            self.relays[relay_index][2].config(text="Closed")  # Update status label to "Closed"

    def find_com_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port,Description,port1 in sorted(ports):
            print("{}".format(port))
            self.port_list.append(port)
    
    def update_relay_stat(self):
        self.interface.current_status = self.interface.read_state()
        if self.interface.current_status == b'0':
            self.relays[0][2].config(text="Closed")
            self.relays[1][2].config(text="Closed")
        elif self.interface.current_status == b'1':
            self.relays[0][2].config(text="Open")
            self.relays[1][2].config(text="Closed")
        elif self.interface.current_status == b'2':
            self.relays[0][2].config(text="Closed")
            self.relays[1][2].config(text="Open")
        elif self.interface.current_status == b'3':
            self.relays[0][2].config(text="Open")
            self.relays[1][2].config(text="Open")

if __name__ == "__main__":
  app = USBRelayManager()
  app.mainloop()