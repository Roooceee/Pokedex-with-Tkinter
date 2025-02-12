import tkinter as tk
import shutil,os
import tkinter.messagebox as tkm
import pickle

from PIL import Image, ImageTk
from class_pokemon import Pokemon
from tkinter import ttk
from tkinter import filedialog as fd

unDictionnairePokemon_chargee = {
}

with open('dictionnairepokemon.pkl', 'ab') as f:
    pickle.dump(unDictionnairePokemon_chargee, f)

list_type = [   "Normal",
                "Feu",
                "Eau",
                "Électrik",
                "Plante",
                "Glace",
                "Combat",
                "Poison",
                "Sol",
                "Vol",
                "Psy",
                "Insecte",
                "Roche",
                "Spectre",
                "Dragon"
]

def choisir_image():
    filetypes = (
        ('Image files', '*.jpeg'),
        ('Image files', '*.jpg'),
        ('Image files', '*.png'),
    )
    filename = fd.askopenfilename(filetypes=filetypes)
    unLabelInputImage.config(text=f"{filename}")

def sauvegarder_image(filename):
    if filename:
        # Définir le dossier de destination
        dossier_destination = "images"
        # Si le dossier n'existe pas, le créer
        if not os.path.exists(dossier_destination):
            os.makedirs(dossier_destination)
        # Extraire le nom du fichier
        nom_fichier = os.path.basename(filename)
        # Créer le chemin de destination
        chemin_destination = os.path.join(dossier_destination, nom_fichier)
        # Copier l'image dans le dossier de destination
        shutil.copy(filename, chemin_destination)
        return chemin_destination
    else:
        print("Aucun fichier sélectionné.")

def ajouter_pokemon():

    with open('dictionnairepokemon.pkl', 'rb') as f:
        unDictionnairePokemon_chargee = pickle.load(f)

    id = uneListeBoxPokemon.size()+1
    nom = unInputNom.get()
    type = uneComboboxType.get()
    taille = unInputTaille.get()
    poid = unInputPoid.get()
    description = unTextAreaInfo.get("1.0",tk.END)
    print(unLabelInputImage.cget("text"))
    image = sauvegarder_image(unLabelInputImage.cget("text"))

    if(nom=="" or type =="" or taille=="" or poid=="" or description=="" or image==""  or type==""):
        tkm.showerror(title="Information manquante" , message="Merci de remplir tout les champs pour ajouter un Pokemon au Pokedex")

    else:
            
            try:

                if nom in unDictionnairePokemon_chargee:
                    tkm.showerror(title="Pokemon déjà présent !", message="Ce Pokemon est déjà présent, doublon impossible !")
                else:
                    taille = float(taille)
                    poid = float(poid)

                    creer_pokemon = Pokemon(id,nom,type,taille,poid,description,image)
                    uneListeBoxPokemon.insert(tk.END,f"{creer_pokemon.nom}")

                    # Ajouter un nouvel objet et réécrire le fichier
                    with open('dictionnairepokemon.pkl', 'rb') as f:
                        unDictionnairePokemon_chargee = pickle.load(f)

                    # Ajouter un nouvel objet
                    unDictionnairePokemon_chargee[nom] = creer_pokemon

                    # Sérialiser à nouveau avec le nouvel objet
                    with open('dictionnairepokemon.pkl', 'wb') as f:
                        pickle.dump(unDictionnairePokemon_chargee, f)


                    tkm.showinfo(title="Pokemon ajouté !" , message="Pokemon ajouté avec succès ! ")

                    unInputNom.delete(0,tk.END)
                    uneComboboxType.set("")
                    unInputPoid.delete(0,tk.END)
                    unInputTaille.delete(0,tk.END)
                    unTextAreaInfo.delete("1.0",tk.END)
                    unLabelInputImage.config(text="")

            except ValueError:
                tkm.showerror(title="Erreur de type" , message="La taille et le poid doivent etre des nombres à virgule !")


def supprimer_pokemon():

    indice = uneListeBoxPokemon.curselection()
    key = uneListeBoxPokemon.get(uneListeBoxPokemon.curselection())

    with open('dictionnairepokemon.pkl', 'rb') as f:
        unDictionnairePokemon_chargee = pickle.load(f)

    print(unDictionnairePokemon_chargee)
    print(unDictionnairePokemon_chargee[key])

    if key in unDictionnairePokemon_chargee:
        del unDictionnairePokemon_chargee[key]
        uneListeBoxPokemon.delete(indice[0],indice[0])

    with open('dictionnairepokemon.pkl', 'wb') as f:
        pickle.dump(unDictionnairePokemon_chargee, f)


def remplir_listbox():

    # Désérialisation (récupérer le dictionnaire depuis le fichier .pickle)
    if os.path.getsize('dictionnairepokemon.pkl') > 0:
        with open('dictionnairepokemon.pkl', 'rb') as f:
            unDictionnairePokemon_chargee = pickle.load(f)

        for i,items in unDictionnairePokemon_chargee.items():
            uneListeBoxPokemon.insert(tk.END,f"{items.nom}") 

def afficher_info_pokemon(event):

    key = uneListeBoxPokemon.get(uneListeBoxPokemon.curselection())

    with open('dictionnairepokemon.pkl', 'rb') as f:
        unDictionnairePokemon_chargee = pickle.load(f)

    unLabelNom.config(text=f"Nom : {unDictionnairePokemon_chargee[key].nom}")
    unLabelType.config(text=f"Type : {unDictionnairePokemon_chargee[key].type}")
    unLabelTaille.config(text=f"Taille en m : {unDictionnairePokemon_chargee[key].taille}")
    unLabelPoid.config(text=f"Poids en kg : {unDictionnairePokemon_chargee[key].poid}")
    unLabelInfo.config(text=f"Description : {unDictionnairePokemon_chargee[key].description}")
    imagePokemon = Image.open(unDictionnairePokemon_chargee[key].UrlImage)
    imagePokemonResized = imagePokemon.resize((300,300))
    imageTk = ImageTk.PhotoImage(imagePokemonResized)
    unLabelImage.config(image=imageTk)
    unLabelImage.image = imageTk




# Fenetre du POKEDEX
unPokedex = tk.Tk()
unPokedex.title("Pokedex")
unPokedex.config(background="white")
unPokedex.rowconfigure([0,1,2],weight=1)
unPokedex.columnconfigure([0, 1, 2],weight=1)

# Entete du POKEDEX
uneFrameEntete = tk.Frame(unPokedex)
uneFrameEntete.grid(row=0, column=0, columnspan=3,sticky="n")

logoPokemon = Image.open("logo/pokemon.png")
logoPokemonResized = logoPokemon.resize((400,200))
imageTklogoPokemon = ImageTk.PhotoImage(logoPokemonResized)
unLabelLogoPokemon = tk.Label(uneFrameEntete, image=imageTklogoPokemon)
unLabelLogoPokemon.grid(row=0, column=0)
unLabelLogoPokemon.config(background="orange")

# Frame Ajouter POKEMON
uneFrameAjouter = tk.Frame(unPokedex)
uneFrameAjouter.grid(row=2, column=0, padx=20 , ipadx=10, sticky="ne")

unLabelNomAjouter = tk.Label(uneFrameAjouter, text="Nom :")
unLabelNomAjouter.grid(row=1, column=0, sticky="we")
unInputNom = tk.Entry(uneFrameAjouter,width=40)
unInputNom.grid(row=1, column=1, pady=10)

unLabelTypeAjouter = tk.Label(uneFrameAjouter, text="Type :")
unLabelTypeAjouter.grid(row=2, column=0, sticky="we")
uneComboboxType = ttk.Combobox(uneFrameAjouter, values=list_type, state="readonly",width=37)
uneComboboxType.grid(row=2, column=1, pady=10)

unLabelTailleAjouter = tk.Label(uneFrameAjouter, text="Taille en m :")
unLabelTailleAjouter.grid(row=3, column=0, sticky="we")
unInputTaille = tk.Entry(uneFrameAjouter,width=40)
unInputTaille.grid(row=3, column=1 , pady=10)

unLabelPoidAjouter = tk.Label(uneFrameAjouter, text="Poids en kg :")
unLabelPoidAjouter.grid(row=4, column=0, sticky="we")
unInputPoid = tk.Entry(uneFrameAjouter,width=40)
unInputPoid.grid(row=4, column=1 , pady=10)

unLabelInfoAjouter = tk.Label(uneFrameAjouter, text="Description :")
unLabelInfoAjouter.grid(row=5, column=0, ipady=5 , sticky="we")
unTextAreaInfo = tk.Text(uneFrameAjouter, width=30, height=5)
unTextAreaInfo.grid(row=5, column=1 , padx=5 , pady=10)

unLabelInputImage = tk.Label(uneFrameAjouter,width=40)
unLabelInputImage.grid(row=6,column=1)
unBoutonImage = tk.Button(uneFrameAjouter,text="Cliquez Ici pour rajouter une image !" , command= choisir_image)
unBoutonImage.grid(row=6,column=0 , padx=10 , sticky="e")

unBoutonAjouter = tk.Button(uneFrameAjouter, text="Ajouter au Pokedex !", command=ajouter_pokemon)
unBoutonAjouter.grid(row=7, column=0, columnspan=2, pady=10 , sticky="se")


# Frame List de POKEMON
uneFrameList = tk.Frame(unPokedex)
uneFrameList.grid(row=2, column=1,sticky="n")
uneFrameList.config(background="white")

uneListeBoxPokemon = tk.Listbox(uneFrameList, height=14, width=30)
uneListeBoxPokemon.grid(row=0, column=0,padx=50,pady=30,sticky="we")

remplir_listbox()
uneListeBoxPokemon.bind("<<ListboxSelect>>", afficher_info_pokemon)

unBoutonSupprimer = tk.Button(uneFrameList,text="Supprimer" , command=supprimer_pokemon)
unBoutonSupprimer.grid(row=1,column=0)

# Frame Info du POKEMON
uneFrameInfo = tk.Frame(unPokedex)
uneFrameInfo.grid(row=2, column=2,sticky="nw")
uneFrameInfo.config(background="white")

uneFrameInfoImage = tk.Frame(uneFrameInfo)
uneFrameInfoImage.grid(row=0,column=0)
uneFrameInfoImage.config(background="white")
unLabelImage = tk.Label(uneFrameInfoImage)
imagePokemon = Image.open("images/Pokemon_Cache.png")
imagePokemonResized = imagePokemon.resize((300,300))
imageTk = ImageTk.PhotoImage(imagePokemonResized)
unLabelImage.config(image=imageTk)
unLabelImage.grid(row=0, column=0,sticky="e")
unLabelImage.config()

uneFrameInfoText = tk.Frame(uneFrameInfo)
uneFrameInfoText.grid(row=0,column=1,padx=20,sticky="e")

unLabelNom = tk.Label(uneFrameInfoText, text="Nom : ???")
unLabelNom.grid(row=0, column=1,padx=5, pady=5)
unLabelType = tk.Label(uneFrameInfoText, text="Type : ???")
unLabelType.grid(row=1, column=1,padx=5, pady=5)
unLabelTaille = tk.Label(uneFrameInfoText, text="Taille : ???")
unLabelTaille.grid(row=2, column=1,padx=5, pady=5)
unLabelPoid = tk.Label(uneFrameInfoText, text="Poids : ???")
unLabelPoid.grid(row=3, column=1,padx=5, pady=5)
unLabelInfo = tk.Label(uneFrameInfoText, text="Description : ???",wraplength=200)
unLabelInfo.grid(row=4, column=1,padx=5, pady=5)

unPokedex.mainloop()
