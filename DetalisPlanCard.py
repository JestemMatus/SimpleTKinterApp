import tkinter as tk
from tkinter import ttk
import KpoRequests
import Waste
from datetime import datetime

class PlannedCardDetails():
    def __init__(self,data):
        self.data = data
        self.search = KpoRequests.Search()
        self.waste_info = None

        if self.data['CarrierCompanyId']:
            self.carrierCompany = self.search.WyszukiwarkaPoCopmanyID(self.data['CarrierCompanyId'])
        else:
            self.carrierCompany = None

        if self.data['ReceiverCompanyId']:
            self.receiverCompany = self.search.WyszukiwarkaPoCopmanyID(self.data['ReceiverCompanyId'])
        else:
            self.receiverCompany = None

        if self.data['ReceiverEupId']:
            self.receiverCompany_eup = self.search.WyszukiwarkaDaneMiejscaPoEUPID(self.data['ReceiverEupId'])
        else:
            self.receiverCompany_eup = None

        self.pesel = "BRAK"
        self.waste = Waste.WasteCode()

        if self.data['WasteCodeId']:
            self.waste_code = self.waste.search_from_list_byId(int(self.data['WasteCodeId']))
            self.waste_info = self.waste.search_code(self.waste_code)
            self.waste_info = self.waste_info[0]
        else:
            self.waste_code = None

        if self.data['WasteProcessId']:
            self.process_id = int(self.data['WasteProcessId'])
            self.process = Waste.WasteProccess()
            self.process_full = self.process.search_in_process(self.process_id)
            self.process_full = self.process_full[0]
        else:
            self.process_full = None
        self.ExtendedWasteDesc = None

        if self.data['WasteGeneratedTerytPk']:
            self.terytId = self.data['WasteGeneratedTerytPk']
            self.teryt = self.search.ZwracaListeGminPoId(self.terytId)
        else:
            self.teryt = None

    def window(self):
        self.TopLevel = tk.Toplevel()
        self.TopLevel.geometry("980x600")

        self.canvas = tk.Canvas(self.TopLevel)
        self.scrollbar = ttk.Scrollbar(self.TopLevel, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.TopLevel.bind("<Configure>", self.on_top_level_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.TopLevel.bind("<MouseWheel>", self.on_mousewheel)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        main_frame = tk.Frame(self.scrollable_frame)
        main_frame.pack(anchor="center")

        self.button1 = ttk.Button(main_frame, text="Przewoźnik", command=self.toggle_frame1, width=158)
        self.button1.pack(pady=2)
        self.frame1 = tk.Frame(main_frame)
        self.frame1_content()

        self.button2 = ttk.Button(main_frame, text="Odbiorca", command=self.toggle_frame2, width=158)
        self.button2.pack(pady=2)
        self.frame2 = tk.Frame(main_frame)
        self.frame2_content()

        self.button3 = ttk.Button(main_frame, text="Odpad", command=self.toggle_frame3, width=158)
        self.button3.pack(pady=2)
        self.frame3 = tk.Frame(main_frame)
        self.frame3_content()

        self.button4 = ttk.Button(main_frame, text="Pozostałe", command=self.toggle_frame4, width=158)
        self.button4.pack(pady=2)
        self.frame4 = tk.Frame(main_frame)
        self.frame4_content()

        self.TopLevel.mainloop()

    def on_top_level_configure(self, event=None):
        self.canvas.itemconfig(self.canvas_frame, width=event.width - self.scrollbar.winfo_width())

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def frame4_content(self):
        self.frame4_internal = tk.Frame(self.frame4, highlightcolor="#0063b1", highlightthickness=1,
                                   highlightbackground="#DCDCDC")
        self.frame4_internal.pack()

        if self.data is None:
            self.VehnicleRegNumber = "BRAK"
            self.PlannedTransportTime = "BRAK"
            self.CertificateNumberAndBoxNumbers = "BRAK"
            self.AdditionalInfo = "BRAK"
            self.IsWasteGenerating = "BRAK"
        else:
            self.VehnicleRegNumber = self.data.get('VehicleRegNumber', "BRAK")
            if len(self.VehnicleRegNumber) < 1:
                self.VehnicleRegNumber = "BRAK"
            else:
                pass
            self.PlannedTransportTime = self.reverse_format_date(str(self.data.get('PlannedTransportTime', "BRAK")))
            if self.PlannedTransportTime == None:
                self.PlannedTransportTime = "BRAK"
            else:
                pass

            self.CertificateNumberAndBoxNumbers = self.data.get('CertificateNumberAndBoxNumbers',"BRAK")
            if self.CertificateNumberAndBoxNumbers == None or len(str(self.CertificateNumberAndBoxNumbers)) < 1:
                self.CertificateNumberAndBoxNumbers = "BRAK"
            else:
                pass

            self.AdditionalInfo = self.data.get('AdditionalInfo',"BRAK")
            if self.AdditionalInfo == None or len(str(self.AdditionalInfo)) < 1:
                self.AdditionalInfo = "BRAK"
            else:
                pass

            self.IsWasteGenerating = self.data.get('IsWasteGenerating',"BRAK")
            if self.IsWasteGenerating == None or len(str(self.IsWasteGenerating)) < 1:
                self.IsWasteGenerating = "BRAK"
            elif self.IsWasteGenerating == True and self.teryt is not None:
                self.IsWasteGenerating = "TAK"
                self.teryt_details()
            elif self.IsWasteGenerating == False:
                self.IsWasteGenerating = "NIE"


        VehiclRegNumber = ttk.Entry(self.frame4_internal, width=52, justify="center", background="white")
        VehiclRegNumber.insert(0, "Numer rejestracyjny pojazdu: "+str(self.VehnicleRegNumber))
        VehiclRegNumber.configure(state="readonly")
        VehiclRegNumber.grid(row=0, column=0, columnspan=1, pady=3, padx=1)

        PlannedTransportTime = ttk.Entry(self.frame4_internal, width=52, justify="center", background="white")
        PlannedTransportTime.insert(0, "Planowany czas transportu: " + str(self.PlannedTransportTime))
        PlannedTransportTime.configure(state="readonly")
        PlannedTransportTime.grid(row=0, column=1, columnspan=1, pady=3, padx=1)

        Cert = ttk.Entry(self.frame4_internal, width=52, justify="center", background="white")
        Cert.insert(0, "Certyfikat i numery paczki: " + str(self.CertificateNumberAndBoxNumbers))
        Cert.configure(state="readonly")
        Cert.grid(row=0, column=2, columnspan=1, pady=3, padx=1)

        Additionalinfo = tk.Text(self.frame4_internal, foreground="black",borderwidth=1, width=136 , height=5, wrap='word', font=("Arial",9), background="#f0f0f0")
        Additionalinfo.insert("1.0", "Dodatkowe informacje: " + str(self.AdditionalInfo))
        Additionalinfo.tag_configure("center", justify='center')
        Additionalinfo.tag_add("center", "1.0", "end")
        Additionalinfo.configure(state="disabled")
        Additionalinfo.grid(row=1, column=0, columnspan=3, pady=3)

        IsGenatingWaste = ttk.Entry(self.frame4_internal, width=160, justify="center", background="white")
        IsGenatingWaste.insert(0, "Czy generuje odpady: " + str(self.IsWasteGenerating))
        IsGenatingWaste.configure(state="readonly")
        IsGenatingWaste.grid(row=2, column=0, columnspan=3, pady=3)

    def frame3_content(self):
        self.frame3_internal = tk.Frame(self.frame3, highlightcolor="#0063b1", highlightthickness=1, highlightbackground="#DCDCDC")
        self.frame3_internal.pack()

        if self.waste_info is None:
            self.wasteCode1 = "BRAK"
            self.waste_code = "BRAK"
            self.danger = "BRAK"
            self.description = 'BRAK'

        else:
            self.wasteCode1 = self.waste_info.get('wasteCodeId', "BRAK")
            self.waste_code = self.waste_info.get('code', "BRAK")
            self.isDangerous = self.waste_info.get('isDangerous', "BRAK")
            if self.isDangerous == True:
                self.danger = "TAK"
            else:
                self.danger = "NIE"

            self.description = self.waste_info.get('description', "BRAK")


        if self.data is None:
            self.WasteMass = "BRAK"
            self.WasteProcessId = "BRAK"
            self.WasteCodeExtendedDescription = "BRAK"
            self.ExtendedWasteCode = "BRAK"
            self.DangerRe = "BRAK"
            self.HazardousWasteReclassification = "BRAK"
            self.HazardousWasteReclassificationDescription = "BRAK"
        else:
            self.WasteMass = self.data.get('WasteMass',"BRAK")
            self.WasteProcessId = self.data.get('WasteProcessId',"BRAK")
            self.HazardousWasteReclassification = self.data.get('HazardousWasteReclassification',
                                                                           "BRAK")
            self.HazardousWasteReclassificationDescription = self.data.get('HazardousWasteReclassificationDescription',
                                                                           "BRAK")
            self.WasteCodeExtendedDescription = self.data.get('WasteCodeExtendedDescription', "BRAK")

        if self.HazardousWasteReclassification == None:
            self.HazardousWasteReclassification = "BRAK"
        elif self.HazardousWasteReclassification == False:
            self.HazardousWasteReclassification = "NIE"
        elif self.HazardousWasteReclassification == True:
            self.HazardousWasteReclassification = "TAK"
            self.dangerDesc()
        else:
            pass

        if self.WasteCodeExtendedDescription == None:
            self.WasteCodeExtendedDescription = "BRAK"
        else:
            pass

        self.WasteCodeExtended = self.data.get('WasteCodeExtended', "BRAK")
        if self.WasteCodeExtended == None:
            self.WasteCodeExtended = "BRAK"
        elif self.WasteCodeExtended == False:
            self.WasteCodeExtended = "NIE"
        elif self.WasteCodeExtended == True:
            self.WasteCodeExtended = "TAK"
            self.create_extend()
        else:
            pass




        if self.process_full is None:
            self.processName = "BRAK"
            self.processDescription = "BRAK"

        else:
            self.processName = self.process_full['codeName']
            self.processDescription = self.process_full['name']


        wasteCodeId = ttk.Entry(self.frame3_internal, width=52, justify="center", background="white")
        wasteCodeId.insert(0, "Id odpadu: " + str(self.wasteCode1))
        wasteCodeId.configure(state="readonly")
        wasteCodeId.grid(row=0, column=0, columnspan=1, pady=3,padx=1)

        wasteCode = ttk.Entry(self.frame3_internal, width=52, justify="center", background="white")
        wasteCode.insert(0, "Kod odpadu: " + str(self.waste_code))
        wasteCode.configure(state="readonly")
        wasteCode.grid(row=0, column=1, columnspan=1, pady=3, padx=1)

        isDangerous = ttk.Entry(self.frame3_internal, width=52, justify="center", background="white")
        isDangerous.insert(0, "Czy niebezpieczny: " + str(self.danger))
        isDangerous.configure(state="readonly")
        isDangerous.grid(row=0, column=2, columnspan=1, pady=3, padx=1)

        description = ttk.Entry(self.frame3_internal, width=158, justify="center", background="white")
        description.insert(0, "Opis: " + str(self.description))
        description.configure(state="readonly")
        description.grid(row=1, column=0, columnspan=3, pady=3, padx=1)


        waste_mass = ttk.Entry(self.frame3_internal, width=52, justify="center", background="white")
        waste_mass.insert(0, "Masa odpadu: " + str(self.WasteMass)+" ton [Mg]")
        waste_mass.configure(state="readonly")
        waste_mass.grid(row=2, column=0, columnspan=1, pady=3, padx=1)

        waste_process = ttk.Entry(self.frame3_internal, width=52, justify="center", background="white")
        waste_process.insert(0, "Id prcesu: " + str(self.WasteProcessId))
        waste_process.configure(state="readonly")
        waste_process.grid(row=2, column=1, columnspan=1, pady=3, padx=1)


        waste_process_name = ttk.Entry(self.frame3_internal, width=52, justify="center", background="white")
        waste_process_name.insert(0, "Nazwa procesu: " + str(self.processName))
        waste_process_name.configure(state="readonly")
        waste_process_name.grid(row=2, column=2, columnspan=1, pady=3, padx=1)

        process_description = ttk.Entry(self.frame3_internal, width=158, justify="center", background="white")
        process_description.insert(0, "Opis: " + str(self.processDescription))
        process_description.configure(state="readonly")
        process_description.grid(row=3, column=0, columnspan=3, pady=3, padx=1)

        ExtendedWasteCode = ttk.Entry(self.frame3_internal, width=158, justify="center", background="white")
        ExtendedWasteCode.insert(0, "Rozszerzony kod odpadów: " + str(self.WasteCodeExtended))
        ExtendedWasteCode.configure(state="readonly")
        ExtendedWasteCode.grid(row=4, column=0, columnspan=3, pady=3, padx=1)

        HazardusWasteRe = ttk.Entry(self.frame3_internal, width=158, justify="center", background="white")
        HazardusWasteRe.insert(0, "Reklasyfikacja jako niebiezpieczny: " + str(self.HazardousWasteReclassification))
        HazardusWasteRe.configure(state="readonly")
        HazardusWasteRe.grid(row=6, column=0, columnspan=3, pady=3, padx=1)

    def frame2_content(self):
        frame2_internal = tk.Frame(self.frame2, highlightcolor="#0063b1", highlightthickness=1, highlightbackground="#DCDCDC")
        frame2_internal.pack(pady=10)

        if self.receiverCompany is None:
            self.ReceiverCompanyIdValue = "BRAK"
            self.ReceiverRegistrationNumber = "BRAK"
            self.name = "BRAK"
            self.nip = "BRAK"
            self.nipEu = "BRAK"
            self.pasel = "BRAK"
        else:
            self.ReceiverCompanyIdValue = self.receiverCompany.get('companyId', "BRAK")
            self.ReceiverRegistrationNumber = self.receiverCompany.get('registrationNumber', "BRAK")
            self.name = self.receiverCompany.get('name',"BRAK")
            self.nip = self.receiverCompany.get('nip',"BRAK")
            self.nipEu = self.receiverCompany.get('nipEu',"BRAK")
            self.pesel = self.receiverCompany.get('pesel',"BRAK")

        if self.receiverCompany_eup is None:
            self.ReceiverCompanyEupValue = "BRAK"
            self.EupName = "BRAK"
            self.address_text = "BRAK"
        else:
            self.ReceiverCompanyEupValue = self.receiverCompany_eup.get('registrationNumber',"BRAK")
            self.EupName = self.receiverCompany_eup.get('name', "BRAK")
            self.address_text = self.receiverCompany_eup.get('address',"BRAK")


        ReceiverCompanyId = ttk.Entry(frame2_internal, width=158, justify="center", background="white")
        ReceiverCompanyId.insert(0, "Id Odbiorcy: " + str(self.ReceiverCompanyIdValue))
        ReceiverCompanyId.configure(state="readonly")
        ReceiverCompanyId.grid(row=0, column=0, columnspan=4, pady=3,padx=1)

        ReceiverCompanyEupId = ttk.Entry(frame2_internal, width=158, justify="center", background="white")
        ReceiverCompanyEupId.insert(0, "EUP Odbiorcy: " + str( self.ReceiverRegistrationNumber))
        ReceiverCompanyEupId.configure(state="readonly")
        ReceiverCompanyEupId.grid(row=1, column=0, columnspan=4, pady=3)


        registrationNumber = ttk.Entry(frame2_internal, width=78, justify="center", background="white")
        registrationNumber.insert(0, "Numer rejestrowy: " + str(self.ReceiverCompanyEupValue))
        registrationNumber.configure(state="readonly")
        registrationNumber.grid(row=2, column=0, columnspan=2,pady=3,padx=1)


        EupName = ttk.Entry(frame2_internal, width=78, justify="center", background="white")
        EupName.insert(0, "Nazwa: " + str(self.EupName))
        EupName.configure(state="readonly")
        EupName.grid(row=2, column=2, columnspan=2, pady=3,padx=1)

        name = ttk.Entry(frame2_internal, width=158, justify="center", background="white")
        name.insert(0, "Nazwa podmiotu: " + str(self.name))
        name.configure(state="readonly")
        name.grid(row=3, column=0, columnspan=4,pady=3)

        nip = ttk.Entry(frame2_internal, width=78, justify="center", background="white")
        nip.insert(0, "NIP podmiotu: " + str(self.nip))
        nip.configure(state="readonly")
        nip.grid(row=4, column=0, columnspan=2,pady=3,padx=1)

        nipEu = ttk.Entry(frame2_internal, width=78, justify="center", background="white")

        nipEu.insert(0, "NIP Europejski podmiotu: " + str(self.nipEu))

        nipEu.configure(state="readonly")
        nipEu.grid(row=4, column=2, columnspan=2,pady=3,padx=1)

        pesel = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        pesel.insert(0, "Pesel: " + str(self.pesel))
        pesel.configure(state="readonly")
        pesel.grid(row=5, column=0, columnspan=1,pady=3)


        address_text = self.address_text
        address_lines = address_text.split(', ')

        kraj = ""
        wojewodztwo = ""
        powiat = ""
        gmina = ""
        miejscowosc = ""
        ulica = ""
        kod_pocztowy = ""

        for line in address_lines:
            if ":" in line:
                key, value = line.split(": ")
                if key == "Kraj":
                    kraj = value
                elif key == "Województwo":
                    wojewodztwo = value
                elif key == "Powiat":
                    powiat = value
                elif key == "Gmina":
                    gmina = value
                elif key == "Miejscowość":
                    miejscowosc = value
                elif key == "Ulica":
                    ulica = value
                elif key == "Kod pocztowy":
                    kod_pocztowy = value
            else:
                pass


        country = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        country.insert(0, "Kraj: " + str(kraj))
        country.configure(state="readonly")
        country.grid(row=5, column=1,columnspan=1,pady=3)

        wojewodztwo = wojewodztwo.lower()

        wojewodztwo_entry = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        wojewodztwo_entry.insert(0, "Województwo: " + str(wojewodztwo))
        wojewodztwo_entry.configure(state="readonly")
        wojewodztwo_entry.grid(row=5, column=2,columnspan=1,pady=3)

        powiat = powiat.lower()

        powiat_entry = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        powiat_entry.insert(0, "Powiat: " + str(powiat))
        powiat_entry.configure(state="readonly")
        powiat_entry.grid(row=5, column=3,columnspan=1,pady=3)

        gmina = gmina.lower()


        gmina_entry = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        gmina_entry.insert(0, "Gmina: " + str(gmina))
        gmina_entry.configure(state="readonly")
        gmina_entry.grid(row=6, column=0,columnspan=1,pady=3)

        miejscowosc_entry = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        miejscowosc_entry.insert(0, "Miejscowość: " + str(miejscowosc))
        miejscowosc_entry.configure(state="readonly")
        miejscowosc_entry.grid(row=6, column=1,columnspan=1,pady=3)

        ulica_entry = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        ulica_entry.insert(0, "Ulica: " + str(ulica))
        ulica_entry.configure(state="readonly")
        ulica_entry.grid(row=6, column=2,columnspan=1,pady=3)

        kod_pocztowy_entry = ttk.Entry(frame2_internal, width=38, justify="center", background="white")
        kod_pocztowy_entry.insert(0, "Kod pocztowy: " + str(kod_pocztowy))
        kod_pocztowy_entry.configure(state="readonly")
        kod_pocztowy_entry.grid(row=6, column=3,columnspan=1,pady=3)

    def frame1_content(self):
        frame1_internal = tk.Frame(self.frame1, highlightcolor="#0063b1", highlightthickness=1,
                                   highlightbackground="#DCDCDC")
        frame1_internal.pack(pady=10)

        if self.carrierCompany is None:
            self.CarrierCompanyId = "BRAK"
            self.CarrierRegistrationNumber = "BRAK"
            self.carrierCompanyName = "BRAK"
            self.carrierCompanyNip = "BRAK"
            self.carrierCompanyNipEu = "BRAK"
            self.carrierCompanyPesel = "BRAK"
            self.carrierCompanyAddress = "BRAK"
        else:
            self.CarrierCompanyId = self.carrierCompany.get('companyId', "BRAK")
            self.CarrierRegistrationNumber = self.carrierCompany.get('registrationNumber', "BRAK")
            self.carrierCompanyName = self.carrierCompany.get('name', "BRAK")
            self.carrierCompanyNip = self.carrierCompany.get('nip', "BRAK")
            self.carrierCompanyNipEu = self.carrierCompany.get('nipEu', "BRAK")
            self.carrierCompanyPesel = self.carrierCompany.get('pesel', "BRAK")
            self.carrierCompanyAddress = self.carrierCompany.get('address', "BRAK")

        CarrierCompanyId = ttk.Entry(frame1_internal, width=158, justify="center", background="white")
        CarrierCompanyId.insert(0, "Id przewoźnika: " + str(self.CarrierCompanyId))
        CarrierCompanyId.configure(state="readonly")
        CarrierCompanyId.grid(row=0, column=0, columnspan=4, pady=3, padx=1)

        registrationNumber = ttk.Entry(frame1_internal, width=158, justify="center", background="white")
        registrationNumber.insert(0, "Numer rejestrowy: " + str(self.CarrierRegistrationNumber))
        registrationNumber.configure(state="readonly")
        registrationNumber.grid(row=1, column=0, columnspan=4, pady=3)

        name = ttk.Entry(frame1_internal, width=158, justify="center", background="white")
        name.insert(0, "Nazwa podmiotu: " + str(self.carrierCompanyName))
        name.configure(state="readonly")
        name.grid(row=2, column=0, columnspan=4, pady=3)

        nip = ttk.Entry(frame1_internal, width=78, justify="center", background="white")
        nip.insert(0, "NIP podmiotu: " + str(self.carrierCompanyNip))
        nip.configure(state="readonly")
        nip.grid(row=3, column=0, columnspan=2, pady=3, padx=1)

        nipEu = ttk.Entry(frame1_internal, width=78, justify="center", background="white")
        nipEu.insert(0, "NIP Europejski podmiotu: " + str(self.carrierCompanyNipEu))
        nipEu.configure(state="readonly")
        nipEu.grid(row=3, column=2, columnspan=2, pady=3, padx=1)

        pesel = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        pesel.insert(0, "Pesel: " + str(self.carrierCompanyPesel))
        pesel.configure(state="readonly")
        pesel.grid(row=5, column=0, columnspan=1, pady=3)

        address_text = self.carrierCompanyAddress
        address_lines = address_text.split(', ')

        kraj = ""
        wojewodztwo = ""
        powiat = ""
        gmina = ""
        miejscowosc = ""
        ulica = ""
        kod_pocztowy = ""

        for line in address_lines:
            if ":" in line:
                key, value = line.split(": ",
                                        1)
                if key == "Kraj":
                    kraj = value
                elif key == "Województwo":
                    wojewodztwo = value
                elif key == "Powiat":
                    powiat = value
                elif key == "Gmina":
                    gmina = value
                elif key == "Miejscowość":
                    miejscowosc = value
                elif key == "Ulica":
                    ulica = value
                elif key == "Kod pocztowy":
                    kod_pocztowy = value
            else:

                pass

        country = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        country.insert(0, "Kraj: " + str(kraj))
        country.configure(state="readonly")
        country.grid(row=5, column=1, columnspan=1, pady=3)

        wojewodztwo = wojewodztwo.lower()

        wojewodztwo_entry = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        wojewodztwo_entry.insert(0, "Województwo: " + str(wojewodztwo))
        wojewodztwo_entry.configure(state="readonly")
        wojewodztwo_entry.grid(row=5, column=2, columnspan=1, pady=3)

        powiat = powiat.lower()

        powiat_entry = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        powiat_entry.insert(0, "Powiat: " + str(powiat))
        powiat_entry.configure(state="readonly")
        powiat_entry.grid(row=5, column=3, columnspan=1, pady=3)

        gmina = gmina.lower()

        gmina_entry = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        gmina_entry.insert(0, "Gmina: " + str(gmina))
        gmina_entry.configure(state="readonly")
        gmina_entry.grid(row=6, column=0, columnspan=1, pady=3)

        miejscowosc_entry = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        miejscowosc_entry.insert(0, "Miejscowość: " + str(miejscowosc))
        miejscowosc_entry.configure(state="readonly")
        miejscowosc_entry.grid(row=6, column=1, columnspan=1, pady=3)

        ulica_entry = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        ulica_entry.insert(0, "Ulica: " + str(ulica))
        ulica_entry.configure(state="readonly")
        ulica_entry.grid(row=6, column=2, columnspan=1, pady=3)

        kod_pocztowy_entry = ttk.Entry(frame1_internal, width=38, justify="center", background="white")
        kod_pocztowy_entry.insert(0, "Kod pocztowy: " + str(kod_pocztowy))
        kod_pocztowy_entry.configure(state="readonly")
        kod_pocztowy_entry.grid(row=6, column=3, columnspan=1, pady=3)

    def toggle_frame1(self):
        if self.frame1.winfo_ismapped():
            self.frame1.pack_forget()
        else:
            self.frame1.pack(fill='x', after=self.button1)

    def toggle_frame2(self):
        if self.frame2.winfo_ismapped():
            self.frame2.pack_forget()
        else:
            self.frame2.pack(fill='x', after=self.button2)

    def toggle_frame3(self):
        if self.frame3.winfo_ismapped():
            self.frame3.pack_forget()
        else:
            self.frame3.pack(fill='x', after=self.button3)

    def toggle_frame4(self):
        if self.frame4.winfo_ismapped():
            self.frame4.pack_forget()
        else:
            self.frame4.pack(fill='x', after=self.button4)

    @staticmethod
    def reverse_format_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def dangerDesc(self):
        self.DangerWasteDesc = tk.Text(self.frame3_internal, foreground="black", borderwidth=1, width=136, height=5,
                                         wrap='word', font=("Arial", 9), background="#f0f0f0")
        self.DangerWasteDesc.insert("1.0",
                                      "Opis niebezpiecznego odpadu: " + str(self.HazardousWasteReclassificationDescription))
        self.DangerWasteDesc.tag_configure("center", justify='center')
        self.DangerWasteDesc.tag_add("center", "1.0", "end")
        self.DangerWasteDesc.configure(state="disabled")
        self.DangerWasteDesc.grid(row=7, column=0, columnspan=3, pady=3)

    def create_extend(self):
        self.ExtendedWasteDesc = tk.Text(self.frame3_internal, foreground="black", borderwidth=1, width=136, height=5,
                                         wrap='word', font=("Arial", 9), background="#f0f0f0")
        self.ExtendedWasteDesc.insert("1.0",
                                      "Opis rozszerzonego kodu odpadu: " + str(self.WasteCodeExtendedDescription))
        self.ExtendedWasteDesc.tag_configure("center", justify='center')
        self.ExtendedWasteDesc.tag_add("center", "1.0", "end")
        self.ExtendedWasteDesc.configure(state="disabled")
        self.ExtendedWasteDesc.grid(row=5, column=0, columnspan=3, pady=3)

    def teryt_details(self):
        PK = self.teryt['PK']
        gmina_r = self.teryt['rodzaj_gminy']
        gmina = self.teryt['gmina']
        powiat = self.teryt['powiat']
        wojewodztwo = self.teryt['wojewodztwo']

        PK_entry = ttk.Entry(self.frame4_internal, width=52, justify="center", background="white")
        PK_entry.insert(0, "Numer teryt: " + str(PK))
        PK_entry.configure(state="readonly")
        PK_entry.grid(row=3, column=0, columnspan=1, pady=3, padx=1)

        wojewodztwo = wojewodztwo.lower()

        woj = ttk.Entry(self.frame4_internal, width=52, justify="center", background="white")
        woj.insert(0, "Województwo: " + str(wojewodztwo))
        woj.configure(state="readonly")
        woj.grid(row=3, column=1, columnspan=1, pady=3, padx=1)

        woj = ttk.Entry(self.frame4_internal, width=52, justify="center", background="white")
        woj.insert(0, "Powiat: " + str(powiat))
        woj.configure(state="readonly")
        woj.grid(row=3, column=2, columnspan=1, pady=3, padx=1)

        woj = ttk.Entry(self.frame4_internal, width=160, justify="center", background="white")
        woj.insert(0, "Gmina: " + str(gmina) + " ("+str(gmina_r+")"))
        woj.configure(state="readonly")
        woj.grid(row=4, column=0, columnspan=3, pady=3, padx=1)

        if self.data['WasteGeneratingAdditionalInfo'] is None or len(str(self.data['WasteGeneratingAdditionalInfo'])) < 1:
            self.WasteGeneratingAdditionalInfo = "BRAK"
        else:
            self.WasteGeneratingAdditionalInfo = self.data['WasteGeneratingAdditionalInfo']

        self.WasteGeneratingAdditionalInfo_Entry = tk.Text(self.frame4_internal, foreground="black", borderwidth=1, width=136, height=5,
                                         wrap='word', font=("Arial", 9), background="#f0f0f0")
        self.WasteGeneratingAdditionalInfo_Entry.insert("1.0",
                                      "Dodatkowy opis generującego odpady: " + str(self.WasteGeneratingAdditionalInfo))
        self.WasteGeneratingAdditionalInfo_Entry.tag_configure("center", justify='center')
        self.WasteGeneratingAdditionalInfo_Entry.tag_add("center", "1.0", "end")
        self.WasteGeneratingAdditionalInfo_Entry.configure(state="disabled")
        self.WasteGeneratingAdditionalInfo_Entry.grid(row=5, column=0, columnspan=3, pady=3)

if __name__ == "__main__":
    app = PlannedCardDetails({'CarrierCompanyId': None, 'ReceiverCompanyId': 'c056dc70-aee3-4c61-8cc6-2546835a1889', 'ReceiverEupId': '573abd61-3843-4ce7-bc35-d6576737f1b4', 'WasteCodeId': 195, 'VehicleRegNumber': 'aSZxcv', 'WasteMass': '2.5216', 'PlannedTransportTime': '2024-02-13T12:49:52.000Z', 'WasteProcessId': '3814', 'CertificateNumberAndBoxNumbers': 'tvybunimo', 'AdditionalInfo': 'awewqe', 'WasteCodeExtended': True, 'WasteCodeExtendedDescription': 'sadsad', 'HazardousWasteReclassification': True, 'HazardousWasteReclassificationDescription': 'asdasd', 'IsWasteGenerating': True, 'WasteGeneratedTerytPk': '1020084', 'WasteGeneratingAdditionalInfo': 'asdas'})
    app.window()