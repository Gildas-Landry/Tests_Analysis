import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2, wilcoxon, chi2_contingency, mannwhitneyu

class HypothesisTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hypothesis Tests")
        
        # Create a style for consistent appearance
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('Result.TFrame', padx=2, background='white', foreground='blue', borderwidth=2, relief="solid")
        self.style.configure('Result.TLabel', font=('Arial', 12), background='white', foreground='blue')
        
        # Add a heading
        self.heading_label = ttk.Label(root, text="Statistical Hypothesis Tests", font=('Arial', 30, 'bold'))
        self.heading_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.heading_label = ttk.Label(root, foreground="blue", text="(cette interface primaire permet d'effectuer le test de kruskal wallis apres avoir selectionne)", font=('italic', 10, 'bold'))
        self.heading_label.grid(row=0, column=0,columnspan=3, rowspan=2, pady=10)
        # Add a combobox to select the test type
        self.test_type_label = ttk.Label(root, text="Select Test Type: (choisir le test a effectuer)")
        self.test_type_label.grid(row=1, column=0, padx=10, pady=5)
        self.test_type = ttk.Combobox(root,width=30,foreground="blue",font=('Arial', 10, 'bold'), values=["Student_Test","Fisher_Test", "MANN_WHITNET_Test", "Wilcoxon Test","Kruskal-Wallis Test",
                                                    "Chi2_Test","Bartlett Test","One-Way ANOVA","Duncan_Test","Two-Way ANOVA without Replication", "Two-Way ANOVA with Replication",
                                                    ])
        self.test_type.grid(row=1, column=1, padx=10, pady=5)
        self.test_type.bind("<<ComboboxSelected>>", self.select_test)
        
        # Entry for significance level
        self.significance_label = ttk.Label(root, text="Significance Level: (seuil de signification exemple: 0.05)")
        self.significance_label.grid(row=3, column=0, padx=10, pady=5)
        self.significance_entry = ttk.Entry(root)
        self.significance_entry.grid(row=3, column=1, padx=10, pady=5)
        self.significance_error_label = ttk.Label(root, text="", foreground='red')
        self.significance_error_label.grid(row=3, column=1, padx=10, pady=0, sticky="s")
        
        # Container for sample entry fields
        self.sample_entries_frame = ttk.Frame(root)
        self.sample_entries_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        
        # Add a button frame
        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        
        # Add a label to display the result
        self.result_frame = ttk.Frame(root, style='Result.TFrame')
        self.result_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        self.result_label = ttk.Label(self.result_frame, text="", style='Result.TLabel', wraplength=600)
        self.result_label.pack(fill="both", expand=True)
        
        # Add a button to add random samples
        #self.add_samples_button = ttk.Button(self.button_frame, text="Add Random Samples", command=self.add_random_samples, width=30)
        #self.add_samples_button.pack(side="left", padx=(0, 5))
        
        
        # Configure row and column weights for responsive layout
        for i in range(7):  # 7 rows
            root.grid_rowconfigure(i, weight=1)
        for i in range(3):  # 3 columns
            root.grid_columnconfigure(i, weight=1)
    
    def select_test(self, event):
        # Clear existing sample entry fields and result
        for child in self.sample_entries_frame.winfo_children():
            child.destroy()
        self.result = None
        self.result_label.config(text="")
        
        # Get the selected test type
        test_type = self.test_type.get()
        
        # Add sample entry fields based on the selected test type
        if test_type == "Two-Way ANOVA without Replication":
            self.show_two_way_anova_withoutre_interface()
        elif test_type == "Bartlett Test":
            self.bartlett_test_interface()
        elif test_type == "Two-Way ANOVA with Replication":
            self.show_two_way_anova_withre_interface()
        elif test_type == "Wilcoxon Test":
            self.wilcoxon_interface()
        elif test_type == "Chi2_Test":
            self.chi2_interface()
        elif test_type == "Fisher_Test":
            self.fisher_interface()
        elif test_type == "Student_Test":
            self.student_interface()
        elif test_type == "MANN_WHITNET_Test":
            self.mann_whithney_interface()
        elif test_type == "One-Way ANOVA":
            self.one_way_anova_interface()
        elif test_type == "Duncan_Test":
            self.duncan_interface()
        else:
            self.add_sample_entry_fields(2)
            
        # Show the Perform Test button if Kruskal-Wallis Test is selected
        if test_type == "Kruskal-Wallis Test":
            # Add a button to perform the test
            self.perform_button = ttk.Button(root, text="Perform Test", command=self.perform_test, width=15)
            self.perform_button.grid(row=5,columnspan=5)
            # Label and entry for sample sizes
            self.sample_size_label = ttk.Label(root, text="Sample Size: (Nombres d'echantillons)")
            self.sample_size_label.grid(row=2, column=0, padx=10, pady=5)
            self.sample_size_entry = ttk.Entry(root)
            self.sample_size_entry.grid(row=2, column=1, padx=10, pady=5)
            
            self.sample_size_error_label = ttk.Label(root, text="", foreground='red')
            self.sample_size_error_label.grid(row=2, column=1, padx=10, pady=0, sticky="s")
            
            # Add a button to set sample size
            self.set_sample_size_button = ttk.Button(root, text="Apply Size", command=self.set_sample_size)
            self.set_sample_size_button.grid(row=2, column=2, padx=10, pady=5, sticky="w")
            
        else:
            self.perform_button.grid_remove()
            self.set_sample_size_button.grid_remove()
    
    def add_sample_entry_fields(self, num_samples):
        for i in range(num_samples):
            label = ttk.Label(self.sample_entries_frame, text=f"Sample {i + 1}: ( Entrez les données séparés par des point virgules)")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(self.sample_entries_frame, width=20)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.sample_entries_frame.grid_columnconfigure(1, weight=1)
    
    def add_random_samples(self):
        # Get the selected test type
        test_type = self.test_type.get()
        
        # Generate random samples and fill the entry fields
        if test_type == "Kruskal-Wallis Test":
            num_samples = len(self.sample_entries_frame.winfo_children())
            for i in range(num_samples):
                sample_data = np.random.randint(0, 100, 10)  # You can adjust sample size and range of random numbers as needed
                entry = self.sample_entries_frame.winfo_children()[i*2 + 1]
                entry.delete(0, tk.END)
                entry.insert(0, ", ".join(str(x) for x in sample_data))
    
    def set_sample_size(self):
        num_samples = int(self.sample_size_entry.get()) if self.sample_size_entry.get() else 3
        if(num_samples < 3):
            messagebox.showerror("Error", " sample size should be > 2 perform Mann Whitney test if sample size = 2")
            return
        else:
            self.sample_size_error_label.config(text="")
            # Clear existing sample entry fields
            for child in self.sample_entries_frame.winfo_children():
                child.destroy()
        
            self.add_sample_entry_fields(num_samples)
            
    #interface poour le test de duncan
    def duncan_interface(self):
        # Styles
        label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
        entry_style = {"font": ("Arial", 14)}
        button_style = {"font": ("Arial", 14, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0}

        class DuncanTestApp:
            def __init__(self_duncan, master_duncan):
                    self_duncan.master_duncan = master_duncan
                    master_duncan.title("Test de Duncan")

                    # Styles
                    label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
                    entry_style = {"font": ("Arial", 14)}
                    button_style = {"font": ("Arial", 14, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0}

                    self_duncan.group_count_label = tk.Label(master_duncan, text="Nombre de groupes :", **label_style)
                    self_duncan.group_count_label.grid(row=0, column=0, sticky='w')

                    self_duncan.group_count_entry = tk.Entry(master_duncan, **entry_style)
                    self_duncan.group_count_entry.grid(row=0, column=1)

                    self_duncan.alpha_label = tk.Label(master_duncan, text="Seuil de signification (alpha) :", **label_style)
                    self_duncan.alpha_label.grid(row=1, column=0, sticky='w')

                    self_duncan.alpha_entry = tk.Entry(master_duncan, **entry_style)
                    self_duncan.alpha_entry.grid(row=1, column=1)

                    self_duncan.data_entries = []

                    self_duncan.submit_button = tk.Button(master_duncan, text="Entrer les données", command=self_duncan.create_data_entries, **button_style)
                    self_duncan.submit_button.grid(row=2, columnspan=2)
            def create_data_entries(self_duncan):
                try:
                    group_count = int(self_duncan.group_count_entry.get())
                    if group_count <= 0:
                        raise ValueError

                    alpha = float(self_duncan.alpha_entry.get())
                    if alpha <= 0 or alpha >= 1:
                        raise ValueError

                    self_duncan.group_count_entry.config(state='disabled')
                    self_duncan.alpha_entry.config(state='disabled')
                    self_duncan.submit_button.config(state='disabled')

                    for i in range(group_count):
                        label = tk.Label(self_duncan.master_duncan, text=f"Données pour le groupe {i+1} (séparées par des virgules):", **label_style)
                        label.grid(row=i+3, column=0, sticky='w')

                        entry = tk.Entry(self_duncan.master_duncan, **entry_style)
                        entry.grid(row=i+3, column=1)
                        self_duncan.data_entries.append(entry)

                    self_duncan.calc_means_button = tk.Button(self_duncan.master_duncan, text="Calculer les moyennes", command=self_duncan.calculate_means, **button_style)
                    self_duncan.calc_means_button.grid(row=group_count+3, columnspan=2)

                except ValueError:
                    messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif de groupes et un seuil de signification (alpha) valide (entre 0 et 1).")

            def calculate_means(self_duncan):
                try:
                    data = []
                    for entry in self_duncan.data_entries:
                        group_data = list(map(float, entry.get().split(',')))
                        if len(group_data) <= 1:
                            raise ValueError
                        data.append(group_data)

                    means = [np.mean(group) for group in data]
                    messagebox.showinfo("Moyennes des groupes", f"Moyennes des groupes :\n{means}")

                    self_duncan.test_button = tk.Button(self_duncan.master_duncan, text="Effectuer le test de Duncan", command=lambda: self_duncan.run_duncan_test(means), **button_style)
                    self_duncan.test_button.grid(row=len(data)+5, columnspan=2)

                except ValueError:
                    messagebox.showerror("Erreur", "Veuillez entrer des données valides (séparées par des virgules) pour chaque groupe et assurez-vous d'avoir au moins deux données par groupe.")

            def run_duncan_test(self_duncan, means):
                try:
                    group_count = len(means)

                    sorted_means = sorted(means)
                    mean_diffs = [sorted_means[i+1] - sorted_means[i] for i in range(group_count-1)]

                    alpha = float(self_duncan.alpha_entry.get())
                    critical_value = stats.ppf(1 - alpha / 2, group_count - 1)

                    significant_pairs = []
                    for i in range(group_count - 1):
                        if mean_diffs[i] > critical_value * np.sqrt(2 * (group_count - 1)):
                            significant_pairs.append((sorted_means[i], sorted_means[i+1]))

                    if significant_pairs:
                        messagebox.showinfo("Résultat du test", f"Les paires de groupes suivantes sont significativement différentes :\n{significant_pairs}")
                    else:
                        messagebox.showinfo("Résultat du test", "Aucune paire de groupes n'est significativement différente.")

                except ValueError:
                    messagebox.showerror("Erreur", "Veuillez entrer un seuil de signification (alpha) valide (entre 0 et 1).")

                
        duncan_window = tk.Toplevel()
        duncan_window.mainloop()
        duncan_app = DuncanTestApp(duncan_window)

    # interface pour anova simple sans replication
    def one_way_anova_interface(self):
        def degreLiberteLoiFisher(v1, v2, alph):
            df_between = v1
            df_within = v2
            alpha = alph

            # Calcul des points critiques
            point_critique = stats.f.ppf(1 - alpha, df_between, df_within)

            return point_critique
        def calculate():
            try:
                n = int(entry_n.get())
                k = int(entry_k.get())
                tab = []
                for i in range(k):
                    Stab = []
                    for u in range(n):
                        val = int(entry_values[i][u].get())
                        Stab.append(val)
                    tab.append(Stab)

                Ti = sum(sum(row) for row in tab)
                Ti2 = sum(sum(row) ** 2 for row in tab)
                Somme_xij = sum(val ** 2 for row in tab for val in row)
                N = n * k
                CF = float((Ti ** 2) / N)
                SSC = float((Ti2 / n) - CF)
                SST = float(Somme_xij - CF)
                SSE = float(SST - SSC)
                DDL_C = k - 1
                DDL_E = N - k
                DDL_To = N - 1
                S1 = SSC / DDL_C
                S2 = SSE / DDL_E
                F = S1 / S2
                degre = float(entry_d.get())
                Fc = degreLiberteLoiFisher(DDL_C, DDL_E, degre)
                
                result = []
                don = []
                don = ["Source de variation","Effet sur les colonnes","Effet sur les lignes","Erreur","Total"]
                result.append(don)
                
                don = []
                don = ["Somme des carrées",SSC,SSE,SST]
                result.append(don)
                
                don = []
                don = ["DDL",DDL_C,DDL_E,DDL_To]
                result.append(don)
                
                don = []
                don = ["Carrer des moyennes", S1,S2," "]
                result.append(don)
                
                don = []
                don = ["Valeur du Test",F," "," "]
                result.append(don)
                
                for i in range(3):
                    for u in range(5):
                        label_p = tk.Label(one_way_window, text=result[u][i])
                        label_p.grid(row=k+9+i, column=u)
                valo = "INRHo' = [0 ; "+ str(Fc) + "]"
                label_l = tk.Label(one_way_window, text= valo)
                label_l.grid(row=12+k, column=2)
                
                if F > Fc or F < 0 :
                    label_e = tk.Label(one_way_window,text = "Ho est rejeté ")
                    label_e.grid(row = 14+k, column= 2)
                else:
                    label_e = tk.Label(one_way_window,text = "Ho est accepté ")
                    label_e.grid(row = 18+k, column= 2)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")

        def create_entry_widgets():
            try:
                n = int(entry_n.get())
                k = int(entry_k.get())
                if n <= 0 or k <= 0:
                    messagebox.showerror("Error", "Please enter positive values for the number of rows and columns.")
                    return
                # Supprimer les anciens widgets d'entrée s'ils existent
                for widget_list in entry_values:
                    for widget in widget_list:
                        widget.destroy()
                entry_values.clear()
                # Créer de nouveaux widgets d'entrée en fonction des nombres de lignes et de colonnes entrés
                label_j = tk.Label(one_way_window, text="Entrer les valeurs dans le tableau")
                label_j.grid(row=4,column=0)
                for i in range(k):
                    entry_values.append([])
                    for j in range(n):
                        entry = tk.Entry(one_way_window)
                        entry.grid(row=j+5, column=i+1)
                        entry_values[i].append(entry)
                button_calculate = tk.Button(one_way_window, text="Calculate", command=calculate)
                button_calculate.grid(row=3, column= 2)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")   

        one_way_window = tk.Toplevel()
        one_way_window.title("One Way ANOVA hypothesis Test")

        label_n = tk.Label(one_way_window, text="Nombre de lignes :")
        label_n.grid(row=0, column=0)
        entry_n = tk.Entry(one_way_window)
        entry_n.grid(row=0, column=1)

        label_k = tk.Label(one_way_window, text="Nombre de colonnes :")
        label_k.grid(row=1, column=0)
        entry_k = tk.Entry(one_way_window)
        entry_k.grid(row=1, column=1)

        label_d = tk.Label(one_way_window, text="Seuil de signification :")
        label_d.grid(row=2, column=0)
        entry_d = tk.Entry(one_way_window)
        entry_d.grid(row=2, column=1)

        button_generate = tk.Button(one_way_window, text="Valider", command=create_entry_widgets)
        button_generate.grid(row=3, column=0)

        entry_values = []


                
    #interface pour effectuer le test de mann whitney
    def mann_whithney_interface(self):
        # Function to perform Mann-Whitney U test
        def perform_mann_whitney(sample1, sample2, test_type,alph):
            try:
                # Convert user input to lists of floats
                sample1 = list(map(float, sample1.split(",")))
                sample2 = list(map(float, sample2.split(",")))

                # Calculate the critical value based on the significance level (alpha)
                n1 = len(sample1)
                n2 = len(sample2)
                u_critical = n1 * n2 / 2 - 1.96 * (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5
                
                # Perform Mann-Whitney U test
                stat, _ = mannwhitneyu(sample1, sample2)

                # Compare the test statistic with the critical value
                if stat > u_critical:
                    result = f"Null Hypothesis accepted at {alph*100}% of significance level"
                else:
                    result = f"Null hypothesis rejected at {alph*100}% of significance level"
                
                # Display result
                messagebox.showinfo("Mann-Whitney U Test Result", f"Test Statistic: {stat}\nCritical Value: {u_critical}\nResult: {result}\n")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric data in both fields")

        # Function to handle button click
        def calculate():
            choice=tail_var.get()
            
            sample1 = entry_sample1.get()
            sample2 = entry_sample2.get()
            alpha = float(entry_alpha.get())
            perform_mann_whitney(sample1, sample2, choice, alpha)

        # Create main window
        man_window = tk.Toplevel()
        man_window.title("Mann-Whitney U Test")

        # Create labels and entry fields for sample data
        label_sample1 = tk.Label(man_window, text="Sample 1:(Entrez les donnees separees par des point virgules)")
        label_sample1.grid(row=0, column=0, padx=5, pady=5)
        entry_sample1 = tk.Entry(man_window, width=50)
        entry_sample1.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        label_sample2 = tk.Label(man_window, text="Sample 2:(Entrez les donnees separees par des point virgules)")
        label_sample2.grid(row=1, column=0, padx=5, pady=5)
        entry_sample2 = tk.Entry(man_window, width=50)
        entry_sample2.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Creating radio option for test type
                
        # Create frame
        frame = ttk.Frame(man_window, padding="20")
        frame.grid(row=2, column=0)

        # Create radio buttons
        tail_var = tk.StringVar()
        one_tail_radio = ttk.Radiobutton(frame, text="One-tailed", variable=tail_var, value='less')
        two_tail_radio = ttk.Radiobutton(frame, text="Two-tailed", variable=tail_var, value='two-sided')

        # Default selection
        tail_var.set('less')

        # Place radio buttons
        one_tail_radio.grid(row=1, column=0, sticky=tk.W)
        two_tail_radio.grid(row=2, column=0, sticky=tk.W)
                
        # Create label and entry field for alpha (significance level)
        label_alpha = tk.Label(man_window, text="Significance Level (alpha):")
        label_alpha.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        entry_alpha = tk.Entry(man_window, width=10)
        entry_alpha.insert(tk.END, "0.05")  # Default alpha value
        entry_alpha.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Create calculate button
        button_calculate = tk.Button(man_window,font=('bold'),text="Calculate", command=calculate)
        button_calculate.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

                    
    #interface pour effectuer le test de student
    def student_interface(self):
        class PairedSampleTestApp:
            def __init__(self_student, master_student):
                self_student.master_student = master_student
                master_student.title("Test de Comparaison de Deux Moyennes sur des Échantillons Appariés")

                style = ttk.Style()
                style.configure('Custom.TButton', font=('Arial', 12), foreground="blue" )

                self_student.label_sample_data_1 = tk.Label(master_student, text="Valeurs de l'échantillon apparié 1 (séparées par des virgules) :", font=("Arial", 12, "bold"), fg="blue")
                self_student.label_sample_data_1.grid(row=0, column=0, padx=10, pady=5)

                self_student.entry_sample_data_1 = tk.Entry(master_student)
                self_student.entry_sample_data_1.grid(row=1, column=0, padx=10, pady=5)

                self_student.label_sample_data_2 = tk.Label(master_student, text="Valeurs de l'échantillon apparié 2 (séparées par des virgules) :", font=("Arial", 12, "bold"), fg="blue")
                self_student.label_sample_data_2.grid(row=0, column=1, padx=10, pady=5)

                self_student.entry_sample_data_2 = tk.Entry(master_student)
                self_student.entry_sample_data_2.grid(row=1, column=1, padx=10, pady=5)

                self_student.label_alpha = tk.Label(master_student, text="Seuil de signification alpha (%) :", font=("Arial", 12, "bold"), fg="blue")
                self_student.label_alpha.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

                self_student.entry_alpha = tk.Entry(master_student)
                self_student.entry_alpha.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

                self_student.button_calculate_test = ttk.Button(master_student, text="Calculer le test", style='Custom.TButton', command=self_student.calculate_test)
                self_student.button_calculate_test.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

            def calculate_test(self_student):
                sample_data_1_str = self_student.entry_sample_data_1.get()
                sample_data_2_str = self_student.entry_sample_data_2.get()
                alpha_str = self_student.entry_alpha.get()

                if not sample_data_1_str or not sample_data_2_str or not alpha_str:
                    messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                    return

                try:
                    # Récupérer les données des échantillons appariés 1
                    sample_data_1 = [float(x.strip()) for x in sample_data_1_str.split(',')]
                    # Récupérer les données des échantillons appariés 2
                    sample_data_2 = [float(x.strip()) for x in sample_data_2_str.split(',')]

                    # Vérifier que les deux tableaux ont la même longueur
                    if len(sample_data_1) != len(sample_data_2):
                        raise ValueError("Les deux tableaux doivent avoir la même longueur.")

                    # Récupérer la taille de l'échantillon
                    n = len(sample_data_1)

                    # Récupérer le seuil de signification alpha à partir du champ d'entrée
                    alpha_percentage = float(alpha_str)
                    # Convertir le seuil de signification en décimal
                    alpha = alpha_percentage / 100

                    # Calculer les différences entre les échantillons appariés
                    differences = [sample_data_1[i] - sample_data_2[i] for i in range(n)]

                    # Calculer la moyenne et l'écart type des différences
                    mean_difference = np.mean(differences)
                    std_dev_difference = np.std(differences, ddof=1)

                    # Calculer la statistique de test
                    t_statistic = mean_difference / (std_dev_difference / np.sqrt(n))

                    # Calculer le point critique
                    degrees_of_freedom = n - 1
                    pcrit = stats.t.ppf(1 - alpha/2, df=degrees_of_freedom)

                    # Interpréter les résultats
                    if -pcrit <= t_statistic <= pcrit:
                        result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les moyennes sont les mêmes."
                    else:
                        result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les moyennes ne sont pas les mêmes."

                    # Afficher les résultats avec les détails
                    details = f"Valeur observée ou calculée : {t_statistic}\nPoint critique : {pcrit}"
                    messagebox.showinfo("Résultats", f"{result}\n\n{details}")

                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))

        class TwoSampleTestApp:
            def __init__(self_student, master_student):
                self_student.master_student = master_student
                master_student.title("Test de Comparaison de Deux Moyennes")

                style = ttk.Style()
                style.configure('Custom.TButton', font=('Arial', 12), foreground='blue')

                self_student.label_data_source = tk.Label(master_student, text="Source des données :", font=("Arial", 12, "bold"), fg="blue")
                self_student.label_data_source.grid(row=0, column=0, padx=10, pady=5)

                self_student.data_source_var = tk.StringVar()
                self_student.data_source_var.set("tableau")
                self_student.radio_table = tk.Radiobutton(master_student, text="Tableau", variable=self_student.data_source_var, value="tableau", command=self_student.show_table_inputs)
                self_student.radio_table.grid(row=0, column=1, padx=5, pady=5)
                self_student.radio_manual = tk.Radiobutton(master_student, text="Donnees explicites", variable=self_student.data_source_var, value="manuel", command=self_student.show_manual_inputs)
                self_student.radio_manual.grid(row=0, column=2, padx=5, pady=5)

                self_student.frame_table_inputs = tk.Frame(master_student)
                self_student.frame_manual_inputs = tk.Frame(master_student)

                self_student.label_sample_data_1 = tk.Label(self_student.frame_table_inputs, text="Données de l'échantillon 1 (séparées par des virgules) :", font=("Arial", 10), fg="black")
                self_student.label_sample_data_1.grid(row=0, column=0, padx=10, pady=5)
                self_student.entry_sample_data_1 = tk.Entry(self_student.frame_table_inputs)
                self_student.entry_sample_data_1.grid(row=0, column=1, padx=5, pady=5)

                self_student.label_sample_data_2 = tk.Label(self_student.frame_table_inputs, text="Données de l'échantillon 2 (séparées par des virgules) :", font=("Arial", 10), fg="black")
                self_student.label_sample_data_2.grid(row=1, column=0, padx=10, pady=5)
                self_student.entry_sample_data_2 = tk.Entry(self_student.frame_table_inputs)
                self_student.entry_sample_data_2.grid(row=1, column=1, padx=5, pady=5)

                self_student.label_alpha = tk.Label(self_student.frame_table_inputs, text="Seuil de signification alpha (en %) :")
                self_student.label_alpha.grid(row=2, column=0, padx=10, pady=5)
                self_student.entry_alpha = tk.Entry(self_student.frame_table_inputs)
                self_student.entry_alpha.grid(row=2, column=1, padx=5, pady=5)
                self_student.entry_alpha.bind('<FocusOut>', self_student.validate_alpha_input)  # Binding de la fonction de validation

                self_student.label_variance = tk.Label(self_student.frame_table_inputs, text="Les variances sont-elles homogènes? (oui/non) :", font=("Arial", 10), fg="black")
                self_student.label_variance.grid(row=3, column=0, padx=10, pady=5)
                self_student.entry_variance = tk.Entry(self_student.frame_table_inputs)
                self_student.entry_variance.grid(row=3, column=1, padx=5, pady=5)

                self_student.frame_table_inputs.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

                self_student.manual_labels = [
                    "Taille échantillon 1 (n1)",
                    "Taille échantillon 2 (n2)",
                    "Moyenne échantillon 1 (X1)",
                    "Moyenne échantillon 2 (X2)",
                    "Variance échantillon 1 (S1²)",
                    "Variance échantillon 2 (S2²)",
                    "Seuil de signification alpha (%)",
                    "Les variances sont-elles homogènes? (oui/non)"
                ]

                self_student.manual_entries = []

                for i, label_text in enumerate(self_student.manual_labels):
                    label = tk.Label(self_student.frame_manual_inputs, text=label_text + " :", font=("Arial", 10), fg="black")
                    label.grid(row=i, column=0, padx=10, pady=5)
                    entry = tk.Entry(self_student.frame_manual_inputs)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    self_student.manual_entries.append(entry)

                self_student.frame_manual_inputs.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

                self_student.button_calculate_test = ttk.Button(master_student, text="Calculer le test", style='Custom.TButton', command=self_student.calculate_test)
                self_student.button_calculate_test.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

            def show_table_inputs(self_student):
                self_student.frame_manual_inputs.grid_remove()
                self_student.frame_table_inputs.grid()

            def show_manual_inputs(self_student):
                self_student.frame_table_inputs.grid_remove()
                self_student.frame_manual_inputs.grid()

            def calculate_test(self_student):
                source = self_student.data_source_var.get()
                if source == 'tableau':
                    sample_data_1_str = self_student.entry_sample_data_1.get()
                    sample_data_2_str = self_student.entry_sample_data_2.get()
                    alpha_str = self_student.entry_alpha.get()
                    variance_str = self_student.entry_variance.get().lower()

                    if not sample_data_1_str or not sample_data_2_str or not alpha_str or not variance_str:
                        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                        return

                    try:
                        # Récupérer les données des échantillons 1
                        sample_data_1 = [float(x.strip()) for x in sample_data_1_str.split(',')]
                        # Récupérer les données des échantillons 2
                        sample_data_2 = [float(x.strip()) for x in sample_data_2_str.split(',')]

                        # Récupérer la taille de chaque échantillon
                        n1 = len(sample_data_1)
                        n2 = len(sample_data_2)

                        # Récupérer le seuil de signification alpha à partir du champ d'entrée
                        alpha_percentage = float(alpha_str)
                        # Convertir le seuil de signification en décimal
                        alpha = alpha_percentage / 100

                        # Calculer la moyenne pour chaque échantillon
                        mean_1 = np.mean(sample_data_1)
                        mean_2 = np.mean(sample_data_2)

                        # Calculer la variance pour chaque échantillon
                        var_1 = np.var(sample_data_1, ddof=1)
                        var_2 = np.var(sample_data_2, ddof=1)

                        # Vérifier si les variances sont homogènes ou non
                        if variance_str == 'oui':
                            # Calculer la statistique de test pour variances homogènes
                            pooled_std_dev = np.sqrt(((n1 - 1) * var_1 + (n2 - 1) * var_2) / (n1 + n2 - 2))
                            t_statistic = (mean_1 - mean_2) / (pooled_std_dev * np.sqrt(1/n1 + 1/n2))
                            degrees_of_freedom = n1 + n2 - 2
                        elif variance_str == 'non':
                            # Calculer la statistique de test pour variances non homogènes
                            t_statistic = (mean_1 - mean_2) / np.sqrt(var_1 / n1 + var_2 / n2)
                            degrees_of_freedom = ((var_1 / n1 + var_2 / n2) ** 2) / ((var_1 ** 2 / (n1 ** 2 * (n1 - 1))) + (var_2 ** 2 / (n2 ** 2 * (n2 - 1))))

                        # Calculer le point critique
                        pcrit = stats.t.ppf(1 - alpha/2, df=degrees_of_freedom)

                        # Interpréter les résultats
                        if -pcrit <= t_statistic <= pcrit:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les moyennes sont les mêmes."
                        else:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les moyennes ne sont pas les mêmes."

                        # Afficher les résultats avec les détails
                        details = f"Valeur observée ou calculée : {t_statistic}\nPoint critique : {pcrit}"
                        messagebox.showinfo("Résultats", f"{result}\n\n{details}")

                    except ValueError as e:
                        messagebox.showerror("Erreur", str(e))
                elif source == 'manuel':
                    alpha_str = self_student.manual_entries[6].get()
                    variance_str = self_student.manual_entries[7].get().lower()

                    if not all(entry.get() for entry in self_student.manual_entries[:-2]) or not alpha_str or not variance_str:
                        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                        return

                    try:
                        n1 = int(self_student.manual_entries[0].get())
                        n2 = int(self_student.manual_entries[1].get())
                        mean_1 = float(self_student.manual_entries[2].get())
                        mean_2 = float(self_student.manual_entries[3].get())
                        var_1 = float(self_student.manual_entries[4].get())
                        var_2 = float(self_student.manual_entries[5].get())
                        alpha_percentage = float(alpha_str)
                        alpha = alpha_percentage / 100

                        # Calcul de la statistique T
                        if variance_str == 'oui':
                            pooled_std_dev = np.sqrt(((n1 - 1) * var_1 + (n2 - 1) * var_2) / (n1 + n2 - 2))
                            t_statistic = (mean_1 - mean_2) / (pooled_std_dev * np.sqrt(1/n1 + 1/n2))
                            degrees_of_freedom = n1 + n2 - 2
                        elif variance_str == 'non':
                            t_statistic = (mean_1 - mean_2) / np.sqrt(var_1 / n1 + var_2 / n2)
                            degrees_of_freedom = ((var_1 / n1 + var_2 / n2) ** 2) / ((var_1 ** 2 / (n1 ** 2 * (n1 - 1))) + (var_2 ** 2 / (n2 ** 2 * (n2 - 1))))

                        # Calcul du point critique
                        pcrit = stats.t.ppf(1 - alpha/2, df=degrees_of_freedom)

                        # Interpréter les résultats
                        if -pcrit <= t_statistic <= pcrit:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les moyennes sont les mêmes."
                        else:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les moyennes ne sont pas les mêmes."

                        # Afficher les résultats avec les détails
                        details = f"Valeur observée ou calculée : {t_statistic}\nPoint critique : {pcrit}"
                        messagebox.showinfo("Résultats", f"{result}\n\n{details}")

                    except ValueError as e:
                        messagebox.showerror("Erreur", str(e))

            def validate_alpha_input(self_student, event):
                new_value = self_student.entry_alpha.get()
                # Vérifier si la nouvelle valeur est composée uniquement de chiffres ou se termine par un pourcentage et est composée de chiffres
                if new_value.isdigit() or (new_value.endswith('%') and new_value[:-1].isdigit()):
                    # Convertir la valeur en entier (en enlevant le signe de pourcentage si présent)
                    value = int(new_value[:-1]) if new_value.endswith('%') else int(new_value)
                    # Vérifier si la valeur est comprise entre 1 et 100 inclusivement
                    if 1 <= value <= 100:
                        return True
                # Afficher une alerte si la valeur est invalide
                messagebox.showerror("Erreur", "Le seuil alpha doit être compris entre 1 et 100 %.")
                return False

        class StudentApplication:
            def __init__(self_student, master_student):
                self_student.master_student = master_student
                master_student.title("Sélection du Test")

                style = ttk.Style()
                style.configure('Custom.TButton', font=('Arial', 12))

                self_student.label_select_test = tk.Label(master_student, text="Sélectionnez le type de test à effectuer :", font=("Arial", 12, "bold"), fg="blue")
                self_student.label_select_test.grid(row=0, column=0, padx=10, pady=5)

                self_student.button_paired_sample_test = ttk.Button(master_student, text="Test sur échantillon apparié", command=self_student.open_paired_sample_test)
                self_student.button_paired_sample_test.grid(row=1, column=0, padx=10, pady=5)

                self_student.button_two_sample_test = ttk.Button(master_student, text="Test sur échantillon indépendant", command=self_student.open_two_sample_test)
                self_student.button_two_sample_test.grid(row=2, column=0, padx=10, pady=5)

            def open_paired_sample_test(self_student):
                paired_sample_test_window = tk.Toplevel(self_student.master_student)
                paired_sample_test_app = PairedSampleTestApp(paired_sample_test_window)

            def open_two_sample_test(self_student):
                two_sample_test_window = tk.Toplevel(self_student.master_student)
                two_sample_test_app = TwoSampleTestApp(two_sample_test_window)

        student_window = tk.Toplevel()
        app = StudentApplication(student_window)

    #interface pour appeler le test de fisher
    def fisher_interface(self):
            
        class VarianceHomogeneityApp:
            
            def show_explicit_inputs(self_fisher):
                self_fisher.frame_table_inputs.grid_remove()
                self_fisher.frame_explicit_inputs.grid()

            def show_table_inputs(self_fisher):
                self_fisher.frame_explicit_inputs.grid_remove()
                self_fisher.frame_table_inputs.grid()

            def calculate_test(self_fisher):
                source = self_fisher.data_source_var.get()
                if source == 'explicit':
                    try:
                        n1 = int(self_fisher.explicit_entries[0].get())
                        n2 = int(self_fisher.explicit_entries[1].get())
                        var1 = float(self_fisher.explicit_entries[2].get())
                        var2 = float(self_fisher.explicit_entries[3].get())
                        alpha_percentage = float(self_fisher.explicit_entries[4].get())

                        alpha = alpha_percentage / 100

                        F_observed = max(var1, var2) / min(var1, var2)

                        # Calculate critical value
                        F_critical = stats.f.ppf(1 - alpha/2, n1 - 1, n2 - 1)

                        if F_observed <= F_critical:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les Variances sont pas les memes"
                        else:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les Variances ne sont pas les memes"

                        messagebox.showinfo("Résultats", result)

                    except ValueError as e:
                        messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour les données explicites.")
                elif source == 'table':
                    try:
                        sample_data_1_str = self_fisher.entry_sample_data_1.get()
                        sample_data_2_str = self_fisher.entry_sample_data_2.get()

                        sample_data_1 = [float(x.strip()) for x in sample_data_1_str.split(',')]
                        sample_data_2 = [float(x.strip()) for x in sample_data_2_str.split(',')]

                        n1 = len(sample_data_1)
                        n2 = len(sample_data_2)

                        var1 = np.var(sample_data_1, ddof=1)
                        var2 = np.var(sample_data_2, ddof=1)

                        alpha_percentage = float(self_fisher.entry_alpha.get())
                        alpha = alpha_percentage / 100

                        F_observed = max(var1, var2) / min(var1, var2)

                        # Calculate critical value
                        F_critical = stats.f.ppf(1 - alpha/2, n1 - 1, n2 - 1)

                        if F_observed <= F_critical:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les Variances sont pas les memes"
                        else:
                            result = f"Au risque de se tromper de {alpha*100}% on peut conclure que les Variances ne sont pas les memes"

                        messagebox.showinfo("Résultats", result)

                    except ValueError as e:
                        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour les échantillons.")
            
            def __init__(self_fisher, master_fisher):
                self_fisher.master_fisher = master_fisher
                master_fisher.title("Test d'homogénéité des variances")

                self_fisher.label_data_source = tk.Label(master_fisher, text="Source des données :", font=("Arial", 12, "bold"))
                self_fisher.label_data_source.grid(row=0, column=0, padx=10, pady=5)

                self_fisher.data_source_var = tk.StringVar()
                self_fisher.data_source_var.set("explicit")
                self_fisher.radio_explicit = tk.Radiobutton(master_fisher, text="Données explicites", variable=self_fisher.data_source_var, value="explicit", command=self_fisher.show_explicit_inputs)
                self_fisher.radio_explicit.grid(row=0, column=1, padx=5, pady=5)
                self_fisher.radio_table = tk.Radiobutton(master_fisher, text="Tableau de données", variable=self_fisher.data_source_var, value="table", command=self_fisher.show_table_inputs)
                self_fisher.radio_table.grid(row=0, column=2, padx=5, pady=5)

                self_fisher.frame_explicit_inputs = tk.Frame(master_fisher)
                self_fisher.frame_table_inputs = tk.Frame(master_fisher)

                self_fisher.explicit_labels = [
                    "Taille échantillon 1 (n1)",
                    "Taille échantillon 2 (n2)",
                    "Variance échantillon 1 (S1^2)",
                    "Variance échantillon 2 (S2^2)",
                    "Seuil de signification alpha (%)"
                ]

                self_fisher.explicit_entries = []

                for i, label_text in enumerate(self_fisher.explicit_labels):
                    label = tk.Label(self_fisher.frame_explicit_inputs, text=label_text + " :", font=("Arial", 10), fg="black")
                    label.grid(row=i, column=0, padx=10, pady=5)
                    entry = tk.Entry(self_fisher.frame_explicit_inputs)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    self_fisher.explicit_entries.append(entry)

                self_fisher.frame_explicit_inputs.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

                self_fisher.label_sample_data_1 = tk.Label(self_fisher.frame_table_inputs, text="Valeurs de l'échantillon 1 (séparées par des virgules) :", font=("Arial", 10))
                self_fisher.label_sample_data_1.grid(row=0, column=0, padx=10, pady=5)
                self_fisher.entry_sample_data_1 = tk.Entry(self_fisher.frame_table_inputs)
                self_fisher.entry_sample_data_1.grid(row=0, column=1, padx=5, pady=5)

                self_fisher.label_sample_data_2 = tk.Label(self_fisher.frame_table_inputs, text="Valeurs de l'échantillon 2 (séparées par des virgules) :", font=("Arial", 10))
                self_fisher.label_sample_data_2.grid(row=1, column=0, padx=10, pady=5)
                self_fisher.entry_sample_data_2 = tk.Entry(self_fisher.frame_table_inputs)
                self_fisher.entry_sample_data_2.grid(row=1, column=1, padx=5, pady=5)

                self_fisher.label_alpha = tk.Label(self_fisher.frame_table_inputs, text="Seuil de signification alpha (%) :", font=("Arial", 10))
                self_fisher.label_alpha.grid(row=2, column=0, padx=10, pady=5)
                self_fisher.entry_alpha = tk.Entry(self_fisher.frame_table_inputs)
                self_fisher.entry_alpha.grid(row=2, column=1, padx=5, pady=5)

                self_fisher.frame_table_inputs.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

                self_fisher.button_calculate_test = tk.Button(master_fisher, text="Calculer le test", command=self_fisher.calculate_test)
                self_fisher.button_calculate_test.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

                        
        fisher_window = tk.Toplevel()
        app = VarianceHomogeneityApp(fisher_window)
        
    
    #interface pour gerer le test de chi-2
    def chi2_interface(self):
        def generate_input_fields(rows, cols):
            # Effacer les anciens champs de saisie
            for widget in chi2_window.winfo_children():
                widget.destroy()

            # Styles
            label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
            entry_style = {"font": ("Arial", 14)}
            button_style = {"font": ("Arial", 14, "bold"), "bd": 0}

            # Ajouter des champs de saisie pour chaque élément du tableau de contingence
            global entries
            entries = []
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    label = tk.Label(chi2_window, text=f"Observed {i+1},{j+1}:", **label_style)
                    label.grid(row=i, column=2*j, padx=5, pady=5)
                    entry = tk.Entry(chi2_window, **entry_style, width=8)
                    entry.grid(row=i, column=2*j+1, padx=5, pady=5)
                    row_entries.append(entry)
                entries.append(row_entries)

            # Ajouter un champ de saisie pour le seuil de signification
            global entry_alpha
            label_alpha = tk.Label(chi2_window, text="Seuil de signification (alpha):", **label_style)
            label_alpha.grid(row=rows+1, column=0, padx=5, pady=5)
            entry_alpha = tk.Entry(chi2_window, **entry_style, width=8)
            entry_alpha.grid(row=rows+1, column=1, padx=5, pady=5)

            # Ajouter un bouton pour lancer le test
            run_button = tk.Button(chi2_window, text="Lancer le test du chi-deux", command=run_chi2_test, **button_style)
            run_button.grid(row=rows+2, column=0, columnspan=2*cols, pady=20)

        def run_chi2_test():
            # Récupérer les données saisies par l'utilisateur
            try:
                observed = []
                for row_entries in entries:
                    row_data = []
                    for entry in row_entries:
                        row_data.append(int(entry.get()))
                    observed.append(row_data)

                observed = np.array(observed)

                # Récupérer le seuil de signification saisi par l'utilisateur
                alpha = float(entry_alpha.get())
                # Vérifier la condition pour le seuil de signification
                if alpha <= 0 or alpha >= 1:
                    messagebox.showerror("Erreur", "Le seuil de signification doit être compris entre 0 et 1 (exclus).")
                    return

                # Effectuer le test du chi-deux
                chi2_stat, p_value_chi2, _, expected = chi2_contingency(observed)

                # Calcul des degrés de liberté
                df = (observed.shape[0] - 1) * (observed.shape[1] - 1)

                # Calcul du point critique
                critical_value = chi2.ppf(1 - alpha, df)

                # Formulation des hypothèses
                hypotheses = "H0 : Il n'y a pas d'association significative entre les variables du tableau de contingence.\n"\
                            "H1 : Il y a une association significative entre les variables du tableau de contingence.\n"

                # Conclusion du test du chi-deux
                if p_value_chi2 < alpha:
                    conclusion_chi2 = f"La p-value est inférieure au seuil de signification {alpha}, donc on rejette H0.\n"\
                                    f" au risque de se tromper de {entry_alpha.get()}% on peut conclure qu'Il y a une association significative entre les variables du tableau de contingence."
                else:
                    conclusion_chi2 = f"La p-value est supérieure au seuil de signification {alpha}, donc on ne rejette pas H0.\n"\
                                    f" au risque de se tromper de {alpha*100}% on peut conclure qu'Il n'y a pas suffisamment de preuves pour conclure à une association significative entre les variables du tableau de contingence."

                # Afficher les résultats dans une boîte de dialogue
                messagebox.showinfo("Résultats du test du chi-deux",
                                    f"Hypothèses :\n{hypotheses}\n"\
                                    f"Statistic chi2 = {chi2_stat}\n"\
                                    f"p-value = {p_value_chi2}\n"\
                                    f"Point critique (alpha={alpha}) = {critical_value}\n"\
                                    f"Degrés de liberté = {df}\n"\
                                    f"Fréquences attendues :\n{expected}\n\n"\
                                    f"Conclusion :\n{conclusion_chi2}")

            except ValueError:
                messagebox.showerror("Erreur", "Veuillez saisir des valeurs entières pour le tableau de contingence et un nombre valide pour le seuil de signification.")

        def get_table_size():
            # Récupérer les dimensions du tableau de contingence
            try:
                rows = int(entry_rows.get())
                cols = int(entry_cols.get())
                generate_input_fields(rows, cols)
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez saisir des valeurs entières pour les dimensions du tableau de contingence.")

        # Créer une fenêtre Tkinter
        chi2_window = tk.Toplevel()
        chi2_window.title("Test du chi-deux")
        chi2_window.configure(background='#f0f0f0')

        # Styles
        label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
        entry_style = {"font": ("Arial", 14)}
        button_style = {"font": ("Arial", 14, "bold"),"bg":"gray", "bd": 0}

        # Ajouter des champs de saisie pour les dimensions du tableau de contingence
        label_rows = tk.Label(chi2_window, text="Nombre de lignes:", **label_style)
        label_rows.grid(row=0, column=0, padx=5, pady=5)
        entry_rows = tk.Entry(chi2_window, **entry_style)
        entry_rows.grid(row=0, column=1, padx=5, pady=5)

        label_cols = tk.Label(chi2_window, text="Nombre de colonnes:", **label_style)
        label_cols.grid(row=1, column=0, padx=5, pady=5)
        entry_cols = tk.Entry(chi2_window, **entry_style)
        entry_cols.grid(row=1, column=1, padx=5, pady=5)

        # Ajouter un bouton pour générer les champs de saisie en fonction des dimensions du tableau
        generate_button = tk.Button(chi2_window, text="Générer le tableau de contingence", command=get_table_size, )
        generate_button.grid(row=2, column=0, columnspan=2, pady=20)


    
    #interface pour gerer le test de wilcoxon
    def wilcoxon_interface(self):
        def generate_input_fields():
            # Effacer les anciens champs de saisie
            for widget in wil_wimdow.winfo_children():
                widget.destroy()

            # Styles
            label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
            entry_style = {"font": ("Arial", 14)}
            button_style = {"font": ("Arial", 14, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0}

            # Ajouter des champs de saisie pour les données
            label_X = tk.Label(wil_wimdow, text="Échantillon X (séparés par des virgules) :", **label_style)
            label_X.grid(row=0, column=0, padx=5, pady=5)
            entry_X = tk.Entry(wil_wimdow, **entry_style)
            entry_X.grid(row=0, column=1, padx=5, pady=5)

            label_Y = tk.Label(wil_wimdow, text="Échantillon Y (séparés par des virgules) :", **label_style)
            label_Y.grid(row=1, column=0, padx=5, pady=5)
            entry_Y = tk.Entry(wil_wimdow, **entry_style)
            entry_Y.grid(row=1, column=1, padx=5, pady=5)

            # Ajouter un champ de saisie pour le seuil de signification
            label_alpha = tk.Label(wil_wimdow, text="Seuil de signification (alpha) :", **label_style)
            label_alpha.grid(row=2, column=0, padx=5, pady=5)
            entry_alpha = tk.Entry(wil_wimdow, **entry_style)
            entry_alpha.grid(row=2, column=1, padx=5, pady=5)

            # Ajouter un bouton pour lancer le test
            run_button = tk.Button(wil_wimdow, text="Lancer le test de Wilcoxon", command=lambda: run_wilcoxon_test(entry_X.get(), entry_Y.get(), entry_alpha.get()), **button_style)
            run_button.grid(row=3, column=0, columnspan=2, pady=20)
            
        def run_wilcoxon_test(X_data, Y_data, alpha):
            try:
                X = [float(x) for x in X_data.split(',')]
                Y = [float(y) for y in Y_data.split(',')]
                alpha = float(alpha)
                if len(X) != len(Y):
                    messagebox.showerror("Erreur", "Les échantillons X et Y doivent avoir la même taille.")
                    return
                # Vérifier la condition pour le seuil de signification
                if alpha <= 0 or alpha >= 1:
                    messagebox.showerror("Erreur", "Le seuil de signification doit être compris entre 0 et 1 (exclus).")
                    return

                statistic, p_value = wilcoxon(X, Y)

                # Afficher les résultats dans une boîte de dialogue
                conclusion = "Il y a une différence significative entre les échantillons." if p_value < alpha else "Il n'y a pas de différence significative entre les échantillons."
                messagebox.showinfo("Résultats du test de Wilcoxon",
                                    f"Statistique du test de Wilcoxon : {statistic:.2f}\n"
                                    f"Valeur p : {p_value:.4f}\n\n"\
                                    f"Seuil de signification (alpha) : {alpha}\n\n"\
                                    f"Conclusion : {conclusion}")
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez saisir des données numériques valides pour les échantillons et le seuil de signification.")
        # Styles
        label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
        entry_style = {"font": ("Arial", 14)}
        button_style = {"font": ("Arial", 14, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0}
        
        # Créer une fenêtre Tkinter
        wil_wimdow = tk.Toplevel()
        wil_wimdow.title("Test de Wilcoxon")
        wil_wimdow.configure(background='#f0f0f0')
        
        # Générer les champs de saisie pour les données
        generate_input_fields()

    # interface pour anova deux replication avec replication
    def show_two_way_anova_withre_interface(self):
        def degreLiberteLoiFisher(v1,v2,alph):
            df_between = v1
            df_within = v2
            alpha = alph

            # Calcul des points critiques
            point_critique = stats.f.ppf(1 - alpha, df_between, df_within)

            return point_critique

        def calculate():
            try:
                r = int(entry_n.get())
                c = int(entry_k.get())
                n =  int(0)
                alph = float(entry_D.get())
                tab = []
                for i in range(c):
                    Stab = []
                    for u in range(r):
                        val = [float(num.strip()) for num in entry_values[i][u].get().split(' ') if num.strip()]
                        Stab.append(val)
                        if n < len(val):
                            n = len(val)
                    tab.append(Stab)
                print(n)
                Tj2 = int(0)
                Tj = int(0)
                Tij = int(0)
                Somme_xij = int(0)
                for i in range(c):
                    tij = int(0)
                    tj = int(0)
                    for u in range(r):
                        lu = int(0)
                        for f in range(n):
                            val = tab[i][u][f]
                            Tj += val
                            lu += val
                            Somme_xij +=val**2
                        tij += lu**2
                        tj +=lu
                    Tij += tij
                    Tj2 += tj**2

                #Somme selon les lignes
                Ti2 = int(0)
                for i in range(r):
                    ti = int(0)
                    for u in range(c):
                        lu = int(0)
                        for j in range(n):
                            val = tab[u][i][j]
                            lu += val
                        ti += lu
                    Ti2 += ti**2
                
                CF = float((Tj**2)/(c*n*r))
                print(CF , Tj)
                #SOMMES DES CARREES---------------------------------
                SSC = float((Tj2/(r*n))-CF)
                SST = float(Somme_xij - CF)
                SSR = float((Ti2/(n*c))-CF)
                SSRC = (Tij/n) - (Tj2/(r*n)) - (Ti2/(n*c)) + CF
                SSE = SST - SSC - SSR - SSRC

                #DDL----------------------------------
                DDL_C = c - 1
                DDL_L = r - 1
                DDL_T = c*r*c - 1
                DDL_E = r*c*(n-1)
                DDL_RC = DDL_L * DDL_C
                #MOYENNE DES CARREE-------------------------------- 
                MSC = SSC / DDL_C
                MSR = SSR / DDL_L
                MSRC = SSRC / DDL_RC
                MSE = SSE / DDL_E
                #VALEUR DU TEST---------------------------------------------------------------------------------------
                Fc = MSC / MSE
                Fr = MSR / MSE
                Frc = MSRC / MSE
                
                Fc_1 = float(degreLiberteLoiFisher(DDL_C,DDL_T,alph))
                Fc_2 = float(degreLiberteLoiFisher(DDL_L,DDL_T,alph))
                Fc_3 = float(degreLiberteLoiFisher(DDL_RC,DDL_T,alph))
                
                result = []
                don = []
                don = ["Source de variation","Effet sur les colonnes","Effet sur les lignes","Inter-action","Erreur","Total"]
                result.append(don)
                
                don = []
                don = ["Somme des carrées",SSC,SSR,SSRC,SSE,SST]
                result.append(don)
                
                don = []
                don = ["DDL",DDL_C,DDL_L,DDL_RC,DDL_E,DDL_T]
                result.append(don)
                
                don = []
                don = ["Carrer des moyennes", MSC,MSR,MSRC,MSE," "]
                result.append(don)
                
                don = []
                don = ["Valeur du Test",Fc,Fr,Frc," "," "]
                result.append(don)
                
                for i in range(6):
                    for u in range(5):
                        label_p = tk.Label(with_repli_window, text=result[u][i])
                        label_p.grid(row=c+6+i, column=u)
                valo = "INRHo' = [0 ; "+ str( Fc_2) + "]"
                valo1 = 'INRHo" = [0 ; ' + str(Fc_1) + "]"
                valo2 = "INRHo''' = [0 ; " + str(Fc_3) + "]"
                label_l = tk.Label(with_repli_window, text= valo)
                label_l.grid(row=14+c, column=2)
                label_d = tk.Label(with_repli_window,text=valo1)
                label_d.grid(row=15+c, column=2)
                label_E = tk.Label(with_repli_window,text=valo2)
                label_E.grid(row=16+c, column=2)
                if Fr > Fc_2 or Fr < 0 :
                    label_e = tk.Label(with_repli_window,text = "Ho' est rejeté ")
                    label_e.grid(row = 18+c, column= 2)
                else:
                    label_e = tk.Label(with_repli_window,text = "Ho' est accepté ")
                    label_e.grid(row = 18+c, column= 2)
                if Fc > Fc_1 or Fc < 0 :
                    label_e = tk.Label(with_repli_window,text = 'Ho" est rejeté ')
                    label_e.grid(row = 19+c, column= 2)
                else:
                    label_e = tk.Label(with_repli_window,text = 'Ho" est accepté ')
                    label_e.grid(row = 19+c, column= 2)
                if Frc > Fc_3 or Fr < 0 :
                    label_e = tk.Label(with_repli_window,text = "Ho''' est rejeté ")
                    label_e.grid(row = 20+c, column= 2)
                else:
                    label_e = tk.Label(with_repli_window,text = "Ho''' est accepté ")
                    label_e.grid(row = 20+c, column= 2)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")


        def create_entry_widgets():
            try:
                r = int(entry_n.get())
                c = int(entry_k.get())
                if r <= 0 or c <= 0:
                    messagebox.showerror("Error", "Please enter positive values for the number of rows and columns.")
                    return
                # Supprimer les anciens widgets d'entrée s'ils existent
                for widget_list in entry_values:
                    for widget in widget_list:
                        widget.destroy()
                entry_values.clear()
                # Créer de nouveaux widgets d'entrée en fonction des nombres de lignes et de colonnes entrés
                label_j = tk.Label(with_repli_window, text="Entrer les valeurs dans le tableau en espacant le dans une meme cellule")
                label_j.grid(row=3,column=0)
                for i in range(c):
                    entry_values.append([])
                    for j in range(r):
                        entry = tk.Entry(with_repli_window)
                        entry.grid(row=j+6, column=i+1)
                        entry_values[i].append(entry)
                button_calculate = tk.Button(with_repli_window, text="Calculate", command=calculate)
                button_calculate.grid(row=4, column=1)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")   

        with_repli_window = tk.Toplevel()
        with_repli_window.title("ANOVA Two Factor With Replication")

        label_n = tk.Label(with_repli_window, text="Nombre de lignes :")
        label_n.grid(row=0, column=0)
        entry_n = tk.Entry(with_repli_window)
        entry_n.grid(row=0, column=1)

        label_k = tk.Label(with_repli_window, text="Nombre de colonnes :")
        label_k.grid(row=1, column=0)
        entry_k = tk.Entry(with_repli_window)
        entry_k.grid(row=1, column=1)

        label_D = tk.Label(with_repli_window, text="Le seuil de signification:")
        label_D.grid(row=3, column=0)
        entry_D = tk.Entry(with_repli_window)
        entry_D.grid(row=3, column=1)

        button_generate = tk.Button(with_repli_window, text="Valider", command=create_entry_widgets)
        button_generate.grid(row=4, column=0)

        entry_values = []

    #fonction qui appelle l'interface pour bartlett
    def bartlett_test_interface(self):

        def create_data_entries():
            try:
                group_count = int(group_count_entry.get())
                if group_count <= 0:
                    raise ValueError

                alpha = float(alpha_entry.get())
                if alpha <= 0 or alpha >= 1:
                    raise ValueError

                group_count_entry.config(state='disabled')
                alpha_entry.config(state='disabled')
                submit_button.config(state='disabled')
            
                for i in range(group_count):
                    label = tk.Label(bartlett_window, text=f"Données pour le groupe {i+1} (séparées par des virgules):", **label_style)
                    label.grid(row=i+3, column=0, sticky='w')

                    entry = tk.Entry(bartlett_window, **entry_style)
                    entry.grid(row=i+3, column=1)
                    data_entries.append(entry)

                test_button = tk.Button(bartlett_window, text="Effectuer le test de Bartlett", command=lambda: run_bartlett_test(alpha), **button_style)
                test_button.grid(row=group_count+3, columnspan=2)

            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif de groupes et un seuil de signification (alpha) valide (entre 0 et 1).")

        def run_bartlett_test(alpha):
            try:
                data = []
                for entry in data_entries:
                    group_data = list(map(float, entry.get().split(',')))
                    if len(group_data) <= 1:
                        raise ValueError
                    data.append(group_data)

                k = len(data)
                n = [len(group) for group in data]
                N = sum(n)
                mean_var = np.mean([np.var(group, ddof=(k-1)) for group in data])
                chi2_statistic = (N - k) * np.log(mean_var) - sum([(ni - 1) * np.log(np.var(group, ddof=(k-1))) for ni, group in zip(n, data)])
                chi2_statistic /= 1 + (1 / (3 * (k - 1))) * (sum([1 / (ni - 1) for ni in n]) - 1 / (N - k))
                degrees_of_freedom = k - 1
                critical_value = chi2.ppf(1-alpha, degrees_of_freedom)

                messagebox.showinfo("Résultat du test", f"La valeur Observée du test du Bartlett est : {chi2_statistic:.2f}\nLe point critique pour alpha={alpha} est : {critical_value:.2f}")

                if chi2_statistic > critical_value:
                    messagebox.showinfo("Conclusion", "nous pouvons conclure que les variances sont significativement différente (Hétéroscédasticité).")
                else:
                    messagebox.showinfo("Conclusion", "nous pouvons conclure que les variances ne sont pas significativement différente (Homoscédasticité).")

            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des données valides (séparées par des virgules) pour chaque groupe et assurez-vous d'avoir au moins deux données par groupe.")

        bartlett_window = tk.Toplevel(root)
        bartlett_window.title("Bartlett Test App")
        
        label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
        entry_style = {"font": ("Arial", 14)}
        button_style = {"font": ("Arial", 14, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0}

        # Styles
        label_style = {"font": ("Arial", 14), "bg": "#f0f0f0"}
        entry_style = {"font": ("Arial", 14)}
        button_style = {"font": ("Arial", 14, "bold"), "bg": "#4CAF50", "fg": "white", "bd": 0}

        group_count_label = tk.Label(bartlett_window, text="Nombre de groupes :", **label_style)
        group_count_label.grid(row=0, column=0, sticky='w')

        group_count_entry = tk.Entry(bartlett_window, **entry_style)
        group_count_entry.grid(row=0, column=1)

        alpha_label = tk.Label(bartlett_window, text="Seuil de signification (alpha) :", **label_style)
        alpha_label.grid(row=1, column=0, sticky='w')

        alpha_entry = tk.Entry(bartlett_window, **entry_style)
        alpha_entry.grid(row=1, column=1)

        data_entries = []

        submit_button = tk.Button(bartlett_window, text="Entrer les données", command=create_data_entries, **button_style)
        submit_button.grid(row=2, columnspan=2)

    #fonction qui appelle l'interface pour anova a deux facteur sans replication
    def show_two_way_anova_withoutre_interface(self):
        def degreLiberteLoiFisher(v1, v2, alph):
            df_between = v1
            df_within = v2
            alpha = alph

            # Calcul des points critiques
            point_critique = stats.f.ppf(1 - alpha, df_between, df_within)

            return point_critique
        
        def calculate():
            try:
                n = int(entry_n.get())
                k = int(entry_k.get())
                tab = []
                for i in range(k):
                    Stab = []
                    for u in range(n):
                        val = int(entry_values[i][u].get())
                        Stab.append(val)
                    tab.append(Stab)

                Ti = sum(sum(row) for row in tab)
                Ti2 = sum(sum(row) ** 2 for row in tab)
                Somme_xij = sum(val ** 2 for row in tab for val in row)
                Tj2 = sum(sum(row[i] for row in tab) ** 2 for i in range(n))
                N = n * k
                print(f" {Ti}  {Ti2}   {N} ")
                CF = float((Ti ** 2) / N)
                SSC = float((Ti2 / n) - CF)
                SST = float(Somme_xij - CF)
                SSR = float((Tj2 / k) - CF)
                SSE = float(SST - SSC - SSR)
                DDL_C = k - 1
                DDL_L = n - 1
                DDL_E = DDL_L * DDL_C
                DDL_To = N - 1
                MSC = SSC / DDL_C
                MSR = SSR / DDL_L
                MSE = SSE / DDL_E
                Fc = MSC / MSE
                Fr = MSR / MSE

                degre = float(entry_d.get())
                Fc_2 = degreLiberteLoiFisher(DDL_C, DDL_E, degre)
                Fc_1 = degreLiberteLoiFisher(DDL_L, DDL_E, degre)
                
                result = []
                don = []
                don = ["Source de variation","Effet sur les colonnes","Effet sur les lignes","Erreur","Total"]
                result.append(don)
                
                don = []
                don = ["Somme des carrées",SSC,SSR,SSE,SST]
                result.append(don)
                
                don = []
                don = ["DDL",DDL_C,DDL_L,DDL_E,DDL_To]
                result.append(don)
                
                don = []
                don = ["Carrer des moyennes", MSC,MSR,MSE," "]
                result.append(don)
                
                don = []
                don = ["Valeur du Test",Fc,Fr," "," "]
                result.append(don)
                
                for i in range(5):
                    for u in range(5):
                        label_p = tk.Label(without_repli_window, text=result[u][i])
                        label_p.grid(row=k+8+i, column=u)
                valo = "INRHo' = [0 ; "+ str( Fc_1) + "]"
                valo1 = 'INRHo" = [0 ; ' + str(Fc_2) + "]"
                label_l = tk.Label(without_repli_window, text= valo)
                label_l.grid(row=12+k, column=2)
                label_d = tk.Label(without_repli_window,text=valo1)
                label_d.grid(row=13+k, column=2)
                
                if Fc > Fc_2 or Fc < 0 :
                    label_e = tk.Label(without_repli_window,text = "Ho' est rejeté ")
                    label_e.grid(row = 20+k, column= 2)
                else:
                    label_e = tk.Label(without_repli_window,text = "Ho' est accepté ")
                    label_e.grid(row = 20+k, column= 2)
                if Fr > Fc_1 or Fr < 0 :
                    label_e = tk.Label(without_repli_window,text = 'Ho" est rejeté ')
                    label_e.grid(row = 21+k, column= 2)
                else:
                    label_e = tk.Label(without_repli_window,text = 'Ho" est accepté ')
                    label_e.grid(row = 21+k, column= 2)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")

        def create_entry_widgets():
            try:
                n = int(entry_n.get())
                k = int(entry_k.get())
                if n <= 0 or k <= 0:
                    messagebox.showerror("Error", "Please enter positive values for the number of rows and columns.")
                    return
                # Supprimer les anciens widgets d'entrée s'ils existent
                for widget_list in entry_values:
                    for widget in widget_list:
                        widget.destroy()
                entry_values.clear()
                # Créer de nouveaux widgets d'entrée en fonction des nombres de lignes et de colonnes entrés
                label_j = tk.Label(without_repli_window, text="Entrer les valeurs dans le tableau")
                label_j.grid(row=5,column=0)
                for i in range(k):
                    entry_values.append([])
                    for j in range(n):
                        entry = tk.Entry(without_repli_window)
                        entry.grid(row=j+7, column=i+1)
                        entry_values[i].append(entry)
                button_calculate = tk.Button(without_repli_window, text="Calculate", command=calculate)
                button_calculate.grid(row=3, column=2)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")   

        without_repli_window = tk.Toplevel(root)
        without_repli_window.title("ANOVA Two Factor Calculator")

        label_n = tk.Label(without_repli_window, text="Nombre de lignes :")
        label_n.grid(row=0, column=0)
        entry_n = tk.Entry(without_repli_window)
        entry_n.grid(row=0, column=1)

        label_k = tk.Label(without_repli_window, text="Nombre de colonnes :")
        label_k.grid(row=1, column=0)
        entry_k = tk.Entry(without_repli_window)
        entry_k.grid(row=1, column=1)

        label_d = tk.Label(without_repli_window, text="Seuil de significationt : ")
        label_d.grid(row=2, column=0)
        entry_d = tk.Entry(without_repli_window)
        entry_d.grid(row=2, column=1)

        button_generate = tk.Button(without_repli_window, text="Valider", command=create_entry_widgets)
        button_generate.grid(row=3, column=0)

        entry_values = []

    def perform_test(self):
        test_type = self.test_type.get()
        sample_lists = []
        
        # Get samples from entry fields
        for entry in self.sample_entries_frame.winfo_children()[1::2]:
            sample_str = entry.get()
            sample = [float(x.strip()) for x in sample_str.split(",")]
            sample_lists.append(sample)
        
        # Perform Kruskal-Wallis Test
        if test_type == "Kruskal-Wallis Test":
            significance_level = float(self.significance_entry.get())
            if significance_level > 0.05 or significance_level < 0.01:
                messagebox.showerror("Error"," Significance level should be between 0.01 and 0.05")
                return
            else:
                self.significance_error_label.config(text="")
                stat, p_value = stats.kruskal(*sample_lists)
                critical_value = chi2.ppf(1-significance_level, len(sample_lists) - 1)
                if(stat > critical_value):
                    conclusion = f"Au risque de se trompler de {significance_level*100}% de seuil de signification l'Hypothese nulle rejeté ce qui veut dire la moyenne des échantillons ne sont pas les même  "
                else:
                    conclusion = f"Au risque de se trompler de {significance_level*100}% de seuil de signification l'Hypothese nulle acceptée ce qui veut dire que la moyenne des echantillons est la même"
                self.result = f"Kruskal-Wallis la valeur du test est : {stat}\n Point critique est : {critical_value} \n {conclusion}"
        
        # Display the result if it's a new test
        if self.result != self.result_label.cget("text"):
            self.result_label.config(text=self.result)

if __name__ == "__main__":
    root = tk.Tk()
    app = HypothesisTestApp(root)
    
    # Center the window
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Configure resizing behavior
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    root.mainloop()
