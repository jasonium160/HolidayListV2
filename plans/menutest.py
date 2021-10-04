import os

participants = {}
numppt = 0

def ParticipantMenu():
    print("""
        Participant Menu
        =================
        [1]. Sign Up
        [2]. Cancel Sign Up
        [3]. View Participants
        [4]. Save Changes
        [5]. Exit
    """)
    try:
        selection = int(input("Choose an option: "))
        if selection ==  1:
            SignUp(numppt)
        elif selection == 2:
            CancelSignUp(participants)
        elif selection == 3:
            ViewParticipants(participants)
        elif selection == 4:
            SaveChanges(participants)
        elif selection == 5:
            exitMenu()
        else:
            print('wait, what? choose one of the numbers from the options!')
            ParticipantMenu()
    except ValueError:
        print('Huh? what happened? Enter a #$%^&* number :/')
        ParticipantMenu()

##----------------------------------------------------------------------------------------------------------------------
def SignUp(numppt):

    print("""
        Participant Sign Up
        ====================
    """)

    while len(participants) < numppt:
        pptName = str(input("Participant Name: ")).strip()
        if pptName == '':
         pptName = None

        startingSlot = int(input("Desired starting slot #[1-" + str(numppt) + "]: "))  
        if startingSlot in participants:
            print('\nError:\n')
            print('Slot #' + str(startingSlot) + ' is filled. Please try another slot for ' + str(pptName) + '\n')
            startingSlot = int(input("Desired starting slot #[1-" + str(numppt) + "]: "))
            participants[startingSlot] = pptName

        participants[startingSlot] = pptName
    
    print("\n=========||Sign Up completed, let's go back to the main menu")    
    ParticipantMenu()

##----------------------------------------------------------------------------------------------------------------------
def CancelSignUp(participants):

    print("""
        Participant Cancellation
        =========================
    """)

    slotToRemove = int(input('Select a slot to remove a participant from: #[1-' + str(len(participants)) + ']'))
    pptToRemove = str(input("\nJust so you know what you're doing, who was in that slot?"))

    if pptToRemove == participants[slotToRemove]:
        del(participants[slotToRemove])
        participants[slotToRemove] = None
        print('Success: \n')
        print(pptToRemove + ' has been removed from slot #' + str(slotToRemove))
        print('\n=======|| Heading back to main menu!')
        ParticipantMenu()
    else:
        print('Error: \n')
        print(pptToRemove + ' is not in that starting slot... try again')
        CancelSignUp(participants)

##----------------------------------------------------------------------------------------------------------------------
def ViewParticipants(participants):
    print("""
        View Participants
        ==================
    """)
    viewfrom = int(input('Which slot you you like to view from, in the range: [1-' + str(len(participants)) + '] ?: ' ))
    
    bottomrange = viewfrom - 5
    if bottomrange <= 0:
        bottomrange = 1

    toprange = viewfrom + 6
    if toprange > len(participants):
        toprange = len(participants)+1

    print('\n| Starting Position : Name |')

    for i in range(bottomrange, toprange):
        if participants.get(i) is None:
            print('     '+str(i), "   :   ", '[empty]')
        else:
            print('     '+str(i), "   :   ", participants[i])


    goBack = str(input('Go back to main? (y/n): ')).lower()
    if goBack == 'y':
        ParticipantMenu()
    else:
        ViewParticipants(participants)

##----------------------------------------------------------------------------------------------------------------------
def SaveChanges(participants):
    import csv

    wantToSave = str(input('Are you ready to save your stuff? [Y/N]: ')).lower()
    if wantToSave == 'y':
        toSave = participants
        with open('savedPPT.csv', 'w') as savefile:
            for key in toSave.keys():
                savefile.write("%s,%s\n"%(key,toSave[key]))
        print('Stuff Saved-----------------back to main menu')
        ParticipantMenu()
    else:
        print('Alright, come back when you are ready!')
        ParticipantMenu()
    
##----------------------------------------------------------------------------------------------------------------------
def exitMenu():
    print("""
        Exit
        =====
        Any unsaved changes will be lost.
    """)
    goBack = str(input('Are you sure you want to leave? [y/n]: ')).lower()
    if goBack == 'y':
        print('\n ===============||---Goodbye---||===============')
        exit
    else:
        ParticipantMenu()

##----------------------------------------------------------------------------------------------------------------------
##----------------------------------------------------------------------------------------------------------------------

print("""
    ---|| Welcome to Tournaments R Us ||---
    =======================================
""")

numppt = int(input('    Start things off by entering the number of participants: '))
print("\n   There are " +str(numppt) + " participant slots now ready for sign-ups!")
print("\n   Let's go to the main menu to take care of this!")
os.system('clear')
ParticipantMenu()

##----------------------------------------------------------------------------------------------------------------------
##----------------------------------------------------------------------------------------------------------------------