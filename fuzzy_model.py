import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# DEFINISI VARIABEL
ph = ctrl.Antecedent(np.arange(0, 14.1, 0.1), 'ph')
kelembaban = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembaban')
nutrisi = ctrl.Antecedent(np.arange(0, 101, 1), 'nutrisi')

kualitas = ctrl.Consequent(np.arange(0, 101, 1), 'kualitas')

# MEMBERSHIP FUNCTION
ph['asam'] = fuzz.trimf(ph.universe, [0, 0, 6.5])
ph['netral'] = fuzz.trimf(ph.universe, [6, 7, 8])
ph['basa'] = fuzz.trimf(ph.universe, [7.5, 14, 14])

kelembaban['kering'] = fuzz.trimf(kelembaban.universe, [0, 0, 40])
kelembaban['sedang'] = fuzz.trimf(kelembaban.universe, [30, 50, 70])
kelembaban['basah'] = fuzz.trimf(kelembaban.universe, [60, 100, 100])

nutrisi['rendah'] = fuzz.trimf(nutrisi.universe, [0, 0, 40])
nutrisi['sedang'] = fuzz.trimf(nutrisi.universe, [30, 50, 70])
nutrisi['tinggi'] = fuzz.trimf(nutrisi.universe, [60, 100, 100])

kualitas['buruk'] = fuzz.trimf(kualitas.universe, [0, 0, 40])
kualitas['cukup'] = fuzz.trimf(kualitas.universe, [30, 50, 70])
kualitas['subur'] = fuzz.trimf(kualitas.universe, [60, 100, 100])

# RULES
rule1  = ctrl.Rule(ph['netral'] & kelembaban['sedang'] & nutrisi['tinggi'], kualitas['subur'])
rule2  = ctrl.Rule(nutrisi['rendah'], kualitas['buruk'])
rule3  = ctrl.Rule(ph['asam'] & nutrisi['rendah'], kualitas['buruk'])
rule4  = ctrl.Rule(kelembaban['sedang'] & nutrisi['sedang'], kualitas['cukup'])
rule5  = ctrl.Rule(ph['netral'] & nutrisi['sedang'], kualitas['cukup'])
rule6  = ctrl.Rule(kelembaban['basah'] & nutrisi['tinggi'], kualitas['subur'])
rule7  = ctrl.Rule(ph['basa'] & nutrisi['rendah'], kualitas['buruk'])
rule8  = ctrl.Rule(ph['netral'] & kelembaban['basah'] & nutrisi['tinggi'], kualitas['subur'])
rule9  = ctrl.Rule(ph['netral'] & kelembaban['basah'] & nutrisi['sedang'], kualitas['cukup'])
rule10 = ctrl.Rule(ph['netral'] & kelembaban['kering'] & nutrisi['tinggi'], kualitas['cukup'])
rule11 = ctrl.Rule(ph['netral'] & kelembaban['kering'] & nutrisi['sedang'], kualitas['buruk'])
rule12 = ctrl.Rule(ph['asam'] & nutrisi['sedang'], kualitas['cukup'])
rule13 = ctrl.Rule(ph['asam'] & nutrisi['tinggi'], kualitas['cukup'])
rule14 = ctrl.Rule(ph['asam'] & kelembaban['kering'], kualitas['buruk'])
rule15 = ctrl.Rule(ph['basa'] & nutrisi['sedang'], kualitas['cukup'])
rule16 = ctrl.Rule(ph['basa'] & nutrisi['tinggi'], kualitas['cukup'])
rule17 = ctrl.Rule(ph['basa'] & kelembaban['kering'], kualitas['buruk'])

# SISTEM
system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7,
    rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17
])
simulasi = ctrl.ControlSystemSimulation(system)

# FUNGSI HITUNG
def hitung_kualitas(ph_val, kelembaban_val, nutrisi_val):
    simulasi.input['ph'] = ph_val
    simulasi.input['kelembaban'] = kelembaban_val
    simulasi.input['nutrisi'] = nutrisi_val

    simulasi.compute()

    hasil = simulasi.output['kualitas']
    if hasil < 40:
        kategori = "Buruk"
    elif hasil < 70:
        kategori = "Cukup"
    else:
        kategori = "Subur"

    return hasil, kategori