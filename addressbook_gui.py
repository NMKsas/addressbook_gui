"""
Author: NMKsas

Simple GUI created during the COMP.CS.100 Programming 1 course
in Tampere University.

This is a simple graphic user interface for an interactive Address book. The
assignment was to create a simple GUI with tkinter and the given materials.

Check the README.txt -file for acknowledged flaws and further
development ideas.

--- SUMMARY ---

This program allows the user to create an own address book. The user can add
and delete contacts. GUI shows the list of user's contacts, and by clicking one
of the names the user can see the rest of the contact information on the right.
The program includes functions to save or load address book information.

The program has two different classes; Address book (GUI) and Contact -class.
Contact -class is for managing user's contacts.

"""


from tkinter import *
from tkinter import messagebox as mb


class Contact:
    """
    This class is for managing the contacts. It contains the contact
    information and methods how to access the information.
    """
    def __init__(self, first_name, last_name, address_rows,
                 phone_number, email):
        """
        Constructor, creates a new Contact -object.
        """
        self.__firstname = first_name
        self.__lastname = last_name
        self.__address = address_rows
        self.__number = phone_number
        self.__email = email

    def printout(self):
        """
        A function for testing purposes
        :return:
        """
        print(self.__firstname)
        print(self.__lastname)
        print(self.__address)
        print(self.__number)
        print(self.__email)

    def get_name(self):
        """
        Returns the name of the contact.
        :return: string, the name of the contact in order: surname first name.
                 If the whole name is unknown, returns "Unknown".
        """
        if self.get_firstname() == "Unknown" and \
                self.get_lastname() == "Unknown":
            return "Unknown"
        elif self.get_firstname() == "Unknown":
            return self.get_lastname()
        elif self.get_lastname() == "Unknown":
            return self.get_firstname()
        else:
            whole_name = f"{self.get_lastname().strip()} " \
                         f"{self.get_firstname().strip()}"
            return whole_name

    def get_firstname(self):
        """
        Returns contact's first name
        :return: string, the first name of the contact
        """
        return self.does_exist(self.__firstname)

    def get_lastname(self):
        """
        Returns contact's last name
        :return: string, the last name of the contact
        """
        return self.does_exist(self.__lastname)

    def get_address(self):
        """
        Returns the address. Address might have multiple rows,
        separated by ",".
        :return: string or list, the address of the contact
        """
        if self.__address == "":
            return "Unknown"
        if "," in self.__address:
            addressrow_list = self.__address.split(",")
            return addressrow_list
        return self.__address

    def does_exist(self, attribute):
        """
        Defines whether the attribute exists or not
        :param attribute: string, attribute in question (name, address, etc.)
        :return: string, the existing attribute or "Unknown"
        """
        if attribute == "":
            return "Unknown"
        else:
            return attribute

    def get_number(self):
        """
        Returns the number of the contact
        :return: string, the number of the contact
        """
        return self.does_exist(self.__number)

    def get_email(self):
        """
        Returns the e-mail address of the contact
        :return: string, the e-mail of the contact
        """
        return self.does_exist(self.__email)


class Addressbook:
    def __init__(self):
        """
        Constructor for a simple Address Book GUI.
        """
        self.__display = Tk()
        self.__display.title("Address Book")
        self.__contacts = {}
        self.__display.columnconfigure(3, pad=100)

        # "Load old address book?" -messagebox
        self.start()

        # LEFT PANEL BUTTONS (add, modify, delete, save, quit)
        # note: modify -command not implemented yet!
        self.__add_button = Button(self.__display, text="Add contact",
                                   command=self.add_contact_window)

        self.__modify_contact_button = Button(self.__display,
                                              text="Modify contact info")

        self.__delete_button = Button(self.__display, text="Delete contact",
                                      command=self.delete_contact_window)

        self.__save_addressbook_button = Button(self.__display,
                                                text="Save Address book",
                                                command=self.save_addressbook)

        self.__quit_button = Button(self.__display, text="Quit",
                                    command=self.quit)

        # MIDDLE PANEL (All contacts -label and listbox + scrollbar)
        self.__contacts_label = Label(self.__display, text="All contacts\n"
                                                           "(select to view)")
        self.__contact_list = Listbox(self.__display)
        self.contactlist_update()
        self.__contact_list.bind('<<ListboxSelect>>', self.show_contact_info)

        self.__scrollbar = Scrollbar(self.__display)
        self.__contact_list.config(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.config(command=self.__contact_list.yview)

        # CONTACT INFO PANEL
        self.__selected_contact_info = Label(self.__display,
                                             text="Contact info")
        self.__contact_info = Listbox(self.__display)

        # GRID LAYOUT:
        # Left panel
        self.__add_button.grid(row=0, column=0, sticky=N+S+W+E)
        self.__modify_contact_button.grid(row=1, column=0, sticky=N+S+W+E)
        self.__delete_button.grid(row=2, column=0, sticky=N+S+W+E)
        self.__save_addressbook_button.grid(row=3, column=0, sticky=N+S+W+E)
        self.__quit_button.grid(row=4, column=0, sticky=N+S+W+E)
        # Middle panel
        self.__contacts_label.grid(row=0, column=1, sticky=N+S+W+E)
        self.__contact_list.grid(row=1, rowspan=4, column=1, sticky=N+S+W+E)
        self.__scrollbar.grid(row=1, column=2, rowspan=4, sticky=N+S)
        # Right panel
        self.__selected_contact_info.grid(row=0, column=3, sticky=N+S+W+E)
        self.__contact_info.grid(row=1, rowspan=4, column=3, sticky=N+S+W+E)
        self.__display.mainloop()

    def start(self):
        """
        Creates a messagebox right after GUI starts: asks whether the user
        wants to load an old address book or not.
        If "yes" is chosen, load_addressbook() function follows.
        """
        respond = mb.askquestion("Load an old address book",
                                 message="Do you want to load an old "
                                         "address book?")
        if respond == 'yes':
            self.load_addressbook()
        else:
            return

    def load_addressbook(self):
        """
        Read the file for old address book contacts. For now the method
        always chooses "addressbook.txt" -file to read.
        Contact information in the file must be formatted in the following way,
        line by line:
        "First name,Last name;Address row 1,Address row 2;e-mail;phone number"
        """
        try:
            file = open(file="addressbook.txt", mode="r")

        except OSError:
            mb.showerror("Error", "Error reading the file!")
            return

        for line in file:
            self.add_from_file(line)

        file.close()

    def add_from_file(self, line):
        """
        Reads a line from the chosen file. Sends information
        further to create_contact() -method.

        Line must be in the following format:
        "First name,Last name;Address row 1,Address row 2;e-mail;Phone number"

        :param line: string, a line to be read from a file
        """
        line = line.strip()
        names, address, email, phone = line.split(";")
        first_name, last_name = names.split(",")

        self.create_contact(first_name, last_name, address, phone, email)

    def create_contact(self, first_name, last_name, address, phone, email):
        """
        Creates a Contact -object from the given information. Saves
        the contact into the contacts dict (self.__contacts).

        :param first_name: string, the first name of the contact
        :param last_name: string, the last name of the contact
        :param address: string OR list; the address OR address rows
        :param phone: string, the phone number of the contact
        :param email: string, the e-mail address of the contact
        """

        new_contact = Contact(first_name, last_name, address, phone, email)
        # if contact is already in the list, returns
        if new_contact.get_name() in self.__contacts:
            return
        else:
            self.__contacts[new_contact.get_name()] = new_contact

    def add_contact_window(self):
        """
        Window for user entry, to add a new contact manually.
        :return:
        """
        contact_window = Tk()
        contact_window.title("Add contact")

        name_label = Label(contact_window, text="First name")
        first_name = Entry(contact_window)
        last_name_label = Label(contact_window, text="Last name")
        last_name = Entry(contact_window)

        address_label = Label(contact_window, text="Address")
        address_row1 = Entry(contact_window)
        address_row2 = Entry(contact_window)

        number_label = Label(contact_window, text="Phone number")
        phone_number = Entry(contact_window)

        email_label = Label(contact_window, text="E-mail")
        email = Entry(contact_window)

        # save button both creates a new contact and closes the window
        save_button = Button(contact_window, text="Save",
                             command=lambda:
                             [self.create_contact(first_name.get(),
                                                  last_name.get(),
                                                  [address_row1.get(),
                                                   address_row2.get()],
                                                  phone_number.get(),
                                                  email.get()),
                              self.contactlist_update(),
                              contact_window.destroy()])
        # button to cancel process
        cancel_button = Button(contact_window, text="Cancel",
                               command=contact_window.destroy)
        # LAYOUT, from up to down
        name_label.grid(row=0, column=0, columnspan=2)
        first_name.grid(row=1, column=0, columnspan=2)
        last_name_label.grid(row=2, column=0, columnspan=2)
        last_name.grid(row=3, column=0, columnspan=2)
        address_label.grid(row=4, column=0, columnspan=2)
        address_row1.grid(row=5, column=0, columnspan=2)
        address_row2.grid(row=6, column=0, columnspan=2)
        number_label.grid(row=7, column=0, columnspan=2)
        phone_number.grid(row=8, column=0, columnspan=2)
        email_label.grid(row=9, column=0, columnspan=2)
        email.grid(row=10, column=0, columnspan=2)
        save_button.grid(row=11, column=0, sticky=N+S+E+W)
        cancel_button.grid(row=11, column=1, sticky=N+S+E+W)
        contact_window.mainloop()

    def delete_contact_window(self):
        """
        Creates another window; asks which contact will be removed
        """
        delete_window = Tk()
        delete_window.title("Delete contact")
        ask_contact_name = Label(delete_window,
                                 text="Insert the name of the\n"
                                      "contact to be deleted\n"
                                      "\n"
                                      "(Lastname Firstname)")
        contact_name = Entry(delete_window)
        delete_button = Button(delete_window, text="Delete",
                               command=lambda:
                               [self.delete_contact(contact_name.get()),
                                delete_window.destroy()])
        # LAYOUT
        ask_contact_name.grid(row=0, column=0)
        contact_name.grid(row=1, column=0, sticky=N + S + W + E)
        delete_button.grid(row=2, column=0, sticky=N+S+W+E)

    def delete_contact(self, name):
        """
        Deletes the contact from the contact dictionary (self.__contacts). If
        the contact is not found, creates an error messagebox.
        """

        if name in self.__contacts:
            del self.__contacts[name]
            # updates the contact list in GUI:
            self.contactlist_update()
        else:
            mb.showerror("Error", "Contact not found!")

    def contactlist_update(self):
        """
        A function which forms a listbox element of all contacts, according
        to the contacts dict.
        """

        index = 1
        # Clears all the past data
        self.__contact_list.delete('0', 'end')
        # Writes a new list
        contact_dict = self.__contacts
        for name in sorted(contact_dict):
            self.__contact_list.insert(index, contact_dict[name].get_name())
            index += 1

    def show_contact_info(self, Event=None):
        """
        When user clicks one of the contacts on the listbox -element,
        this function shows the further contact information on the right info
        panel
        """
        # Deletes previous information
        self.__contact_info.delete('0', 'end')
        ndex = self.__contact_list.curselection()
        try:
            selected_contact = self.__contact_list.get(ndex)
        except TclError:
            return

        # helper variable
        contact = self.__contacts[selected_contact]

        # Inserting rows for info panel:

        self.__contact_info.insert('end', contact.get_name())

        # if address is a list of multiple address rows,
        # rows are added with for -loop
        address = contact.get_address()
        if isinstance(address, list):
            for row in address:
                self.__contact_info.insert('end', row)
        else:
            self.__contact_info.insert('end', address)

        self.__contact_info.insert('end', contact.get_number())
        self.__contact_info.insert('end', contact.get_email())

    def save_addressbook(self):
        """
        Saves the new address book, overwrites the old file "addressbook.txt".
        :return:
        """
        try:
            save_file = open(file="addressbook.txt", mode="w").close()
            save_file = open(file="addressbook.txt", mode="w")
        except OSError:
            print("Error saving the file!")
            return

        for contact in sorted(self.__contacts):
            contact = self.__contacts[contact]
            first_name = contact.get_firstname()
            last_name = contact.get_lastname()
            email = contact.get_email()

            address = contact.get_address()
            # if address is a list, contains multiple rows:
            if isinstance(address, list):
                address = ",".join(address)

            phone = contact.get_number()
            print(f"{first_name},{last_name};{address};{email};{phone}",
                  file=save_file)

        save_file.close()

    def quit(self):
        """
        Exists the program
        """
        self.__display.destroy()

    def show_contacts(self):
        """
        Test function to print all the contacts.
        """
        for contact in sorted(self.__contacts):
            self.__contacts[contact].printout()
            print()


def main():
    interactive_addressbook = Addressbook()


if __name__ == "__main__":
    main()