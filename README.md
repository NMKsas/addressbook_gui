# GUI for Address book 

Author: NMKsas <br>
December 2020

*Created as an assignment during Programming I -course in Tampere University.*

## Summary

This program allows the user to create an own address book. The user can add
and delete contacts. GUI shows the list of user's contacts, and by clicking one
of the names the user can see the rest of the contact information on the right.
The program includes functions to save or load address book information.

The program has two different classes; Address book (GUI) and Contact -class.
Contact -class is for managing user's contacts.

## Functions to be added

- Modify contact info: implemention?
- Load phonebook from file 

## Issues to be solved/developed further, alterations:

- alternative solution for listbox showing the contact info:
    * removing the selection from listbox 1 doesn't delete the contact info on
      on the right instantly?
- different errors
- flexibility: * which information is necessary for creating a contact?
               * in which cases, error message is shown?
               * force name as an obligatory info (-> no unknown entries)!
- program lets user choose the address book -file, and creates a new .txt file
- better solution for deleting contacts
    * list of contacts, where user selects a contact + delete button?
- Entry() for phone number includes a spot for area code?
- Adding photos to different contacts? -> Panel 4 for photo

## Things to look into:

- multiple windows on Tkinter; the most efficient way to create and manage them
- enhancing the GUI:
	* add- and delete windows
- separating save/load -functions out of the class (?)
    * file management, the most efficient way to deal with it?
- what is the best way to manage listbox -element: removing all previous
  information and filling the list again OR avoiding the duplicates some other
  way
- if one was to use this kind of program, what about security? (a collection of 
  personal information; harmless in a real address book)
