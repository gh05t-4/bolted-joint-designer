#!/usr/bin/env python3

## Program to design lap joint, single cover and double cover butt joint.
## Created by GH057.

# IS 800:2007 codebook reference.

from sys import exit
from math import sqrt, pi

## Class defination for designing the joints.
class JointDesign():

    def __init__(self, data):
        """Constructor to initialize the given data to a dictionary"""
        self.data = data

    def lap_joint(self):
        """Lap joint method definition"""

        ## 1) Shear Strength

        Asb = round((pi * self.data['d']**2) / 4) # nominal plain shank area of the bolt

        Anb = 0.78 * Asb # net shear area of the bolt at threads

        # design strength of the bolt
        V_dsb = (self.data['fub'] / (sqrt(3) * 1.25)) * ((self.data['n_n'] * Anb) + (self.data['n_s'] * Asb)) / 1000

        ## 2) Bearing Strength

        # minimum value of kb
        kb = min([(self.data['e'] / (3 * self.data['d0'])), ((self.data['p'] / (3 * self.data['d0'])) - 0.25), (self.data['fub'] / self.data['fu']), 1])

        # minimum value of t
        t = min([self.data['t1'], self.data['t2']])

        # design bearing strength of a bolt
        V_dpb = (2.5 * kb * self.data['d'] * t * self.data['fu']) / (1.25 * 1000)

        bolt_value = min([round(V_dsb, 2), round(V_dpb, 2)])

        num_bolts = self.data['FL'] / bolt_value # number of bolts required

        # Rounding of the number of bolts to correct value
        if int(num_bolts) % 2 != 0:
            num_bolts = int(num_bolts) + 1
        else:
            num_bolts = int(num_bolts) + 2

        return round(V_dsb, 2), round(V_dpb, 2), num_bolts, self.data['p'], self.data['e']

    def scb_joint(self):
        """single cover butt joint method definition"""

        # 1) Shear Strength

        Asb = round((pi * self.data['d']**2) / 4)

        Anb = 0.78 * Asb

        V_dsb = (self.data['fub'] / (sqrt(3) * 1.25)) * ((self.data['n_n'] * Anb) + (self.data['n_s'] * Asb)) / 1000

        # 2) Bearing Strength

        kb = min([(self.data['e'] / (3 * self.data['d0'])), ((self.data['p'] / (3 * self.data['d0'])) - 0.25), (self.data['fub'] / self.data['fu']), 1])

        t = min([self.data['t1'], self.data['t2'], self.data['t_c']]) # thickness of cover plate included

        V_dpb = (2.5 * kb * self.data['d'] * t * self.data['fu']) / (1.25 * 1000)

        bolt_value = min([round(V_dsb, 2), round(V_dpb, 2)])

        num_bolts = self.data['FL'] / bolt_value

        if int(num_bolts) % 2 != 0:
            num_bolts = int(num_bolts) + 1
        else:
            num_bolts = int(num_bolts) + 2

        return round(V_dsb, 2), round(V_dpb, 2), num_bolts, self.data['p'], self.data['e']

    def dcb_joint(self):
        """double cover butt joint method definition"""
        # 1) Shear Strength

        Asb = round((pi * self.data['d']**2) / 4)

        Anb = 0.78 * Asb

        # check if beta pk is present and multiply the factor accordingly
        if 'B_pk' in self.data.keys():
            V_dsb = (self.data['fub'] / (sqrt(3) * 1.25)) * ((self.data['n_n'] * Anb) + (self.data['n_s'] * Asb)) * self.data['B_pk'] / 1000
        else:
            V_dsb = (self.data['fub'] / (sqrt(3) * 1.25)) * ((self.data['n_n'] * Anb) + (self.data['n_s'] * Asb)) / 1000

        # 2) Bearing Strength

        kb = min([(self.data['e'] / (3 * self.data['d0'])), ((self.data['p'] / (3 * self.data['d0'])) - 0.25), (self.data['fub'] / self.data['fu']), 1])

        t = min([self.data['t1'], self.data['t2'], self.data['t_c'] * 2]) # covering plate thickness * 2

        V_dpb = (2.5 * kb * self.data['d'] * t * self.data['fu']) / (1.25 * 1000)

        bolt_value = min([round(V_dsb, 2), round(V_dpb, 2)])

        num_bolts = self.data['FL'] / bolt_value

        if int(num_bolts) % 2 != 0:
            num_bolts = int(num_bolts) + 1
        else:
            num_bolts = int(num_bolts) + 2

        return round(V_dsb, 2), round(V_dpb, 2), num_bolts, self.data['p'], self.data['e']

    def __str__(self):
        return "Object of class <JointDesign>"
## End of class

def given_data():
    """Input validation of the given data and return it as a dictionary"""

    print()

    try:
    
        # Diameter of the bolt.
        while True:
            try:
                d = int(input("Enter the diameter of the bolt in mm (Eg: 16): "))
                break
            except ValueError:
                print("Please input integer only.")
                continue
        
        # Width of the plate.
        while True:
            try:
                b = int(input("Enter the width of the plate in mm (Eg: 200): "))
                break
            except ValueError:
                print("Please input integer only.")
                continue
        
        # Thickness of the 1st plate.
        while True:
            try:
                t1 = int(input("Enter the thickness of the 1st plate in mm (Eg: 10): "))
                break
            except ValueError:
                print("Please input integer only.")
                continue
        
        # Thickness of the 2nd plate.
        while True:
            try:
                t2 = int(input("Enter the thickness of the 2nd plate in mm (Eg: 18): "))
                break
            except ValueError:
                print("Please input integer only.")
                continue

        # Factored Load.
        while True:
            try:
                FL = int(input("Enter the factored load in kN (Eg: 150): "))
                break
            except ValueError:
                print("Please input integer only.")
                continue

        # Grade of the Bolt.
        while True:
            try:
                b_grade = float(input("Enter the grade of the bolt (Eg: 4.6): "))
                break
            except ValueError:
                print("Please input float only.")
                continue

        # Grade of the Plate.
        while True:
            try:
                p_grade = int(input("Enter the grade of the plate (Eg: 410): "))
                break
            except ValueError:
                print("Please input integer only.")
                continue

        ## Value for diameter of the hole.
        # pg no. 73; Table 19 clause 10.2.1
        if d in range(12, 15):
            d0 = d + 1
        elif d in range(16, 23):
            d0 = d + 2
        elif d == 24:
            d0 = d + 2
        elif d > 24:
            d0 = d + 3
        else:
            print("Diameter of the bolt in invalid.")
            exit(1)
        
        # Edge distance.
        while True:
            e_res = input("Is the edge distance given? [Y/n] ")
            if e_res.lower() == 'y':
                while True:
                    try:
                        edge_dist = int(input("Enter the edge distance in mm (Eg: 30): "))
                        break
                    except ValueError:
                        print("Please input integer only.")
                        continue
                break
            elif e_res.lower() == 'n':
                edge_dist = 1.5 * d0
                break
        
        # Pitch distance.
        while True:
            p_res = input("Is the pitch distance given? [Y/n] ")
            if p_res.lower() == 'y':
                while True:
                    try:
                        pitch_dist = int(input("Enter the pitch distance in mm (Eg: 40): "))
                        break
                    except ValueError:
                        print("Please input integer only.")
                        continue
                break
            elif p_res.lower() == 'n':
                pitch_dist = 2.5 * d
                break

        fub = int(b_grade) * 100 # ultimate tensile strength of bolt
    
    except KeyboardInterrupt:
        print("\nBye..")
        exit(0)

    # returning the data as a dictionary
    return {'d': d, 'b': b, 't1': t1, 't2': t2, 'FL': FL, 'b_grade': b_grade, 'fub': fub, 'fu': p_grade, 'd0': d0, 'e': edge_dist, 'p': pitch_dist}

# definition of lap function
def lap():
    """Creating an instance of JointDesign class to access lap_joint method"""
    data = given_data()

    while True:
        try:
            n_n = int(input("Enter the no. of shear planes with threads n_n (Eg: 1): "))
            data['n_n'] = n_n
            break
        except ValueError:
            print("Please input integer only.")
            continue
    
    while True:
        try:
            n_s = int(input("Enter the no. of shear planes without threads n_s (Eg: 0): "))
            data['n_s'] = n_s
            break
        except ValueError:
            print("Please input integer only.")
            continue

    des = JointDesign(data) # instance of the class

    return des.lap_joint()

# definition of scb function
def scb():
    """Creating an instance of JointDesign class to access scb_joint method"""
    data = given_data()

    while True:
        try:
            n_n = int(input("Enter the no. of shear planes with threads n_n (Eg: 0): "))
            data['n_n'] = n_n
            break
        except ValueError:
            print("Please input integer only.")
            continue
    
    while True:
        try:
            n_s = int(input("Enter the no. of shear planes without threads n_s (Eg: 1): "))
            data['n_s'] = n_s
            break
        except ValueError:
            print("Please input integer only.")
            continue

    # Thickness of the cover plate
    while True:
        try:
            t_c = int(input("Enter the thickness of cover plate in mm (Eg: 8): "))
            data['t_c'] = t_c
            break
        except ValueError:
            print("Please input integer only.")
            continue

    des = JointDesign(data)

    return des.scb_joint()

# definition of dcb funtion
def dcb():
    """Creating an instance of JointDesign class to access dcb_joint method"""
    data = given_data()

    while True:
        try:
            n_n = int(input("Enter the no. of shear planes with threads n_n (Eg: 1): "))
            data['n_n'] = n_n
            break
        except ValueError:
            print("Please input integer only.")
            continue
    
    while True:
        try:
            n_s = int(input("Enter the no. of shear planes without threads n_s (Eg: 1): "))
            data['n_s'] = n_s
            break
        except ValueError:
            print("Please input integer only.")
            continue

    while True:
        try:
            t_c = int(input("Enter the thickness of cover plates in mm (Eg: 8): "))
            data['t_c'] = t_c
            break
        except ValueError:
            print("Please input integer only.")
            continue

    # Check for packing plate and Beta pk
    while True:
        pack_plate = input("Is the packing plate required? [Y/n] ")
        if pack_plate.lower() == 'y':
            while True:
                try:
                    t_pk = int(input("Enter the thickness of packing plate in mm (Eg: 8): "))
                    data['t_pk'] = t_pk
                    if abs(data['t1'] - data['t2']) > 6:
                        B_pk = 1 - (0.0125 * t_pk)
                        data['B_pk'] = B_pk
                    break
                except ValueError:
                    print("Please input integer only.")
                    continue
            break
        elif pack_plate.lower() == 'n':
            break

    des = JointDesign(data)

    return des.dcb_joint()

def display_results(design_vals):
    print()
    print("#" * 25)
    print()
    print("Design Values are:")
    print(f"V_dsb        = {design_vals[0]} kN")
    print(f"V_dpb        = {design_vals[1]} kN")
    print(f"No. of bolts = {design_vals[2]} no's")
    print(f"pitch, p     = {design_vals[3]} mm")
    print(f"edge, e      = {design_vals[4]} mm")
    print()
    print("#" * 25)

# definition of main function
def main():
    print("""
        ██████╗ ██████╗██╗ █████████████████████╗      
        ██╔══████╔═══████║ ╚══██╔══██╔════██╔══██╗     
        ██████╔██║   ████║    ██║  █████╗ ██║  ██║     
        ██╔══████║   ████║    ██║  ██╔══╝ ██║  ██║     
        ██████╔╚██████╔█████████║  █████████████╔╝     
        ╚═════╝ ╚═════╝╚══════╚═╝  ╚══════╚═════╝      
                                                       
                 ██╗██████╗█████╗   ██████████╗        
                 ████╔═══████████╗  ██╚══██╔══╝        
                 ████║   ██████╔██╗ ██║  ██║           
            ██   ████║   ██████║╚██╗██║  ██║           
            ╚█████╔╚██████╔████║ ╚████║  ██║           
             ╚════╝ ╚═════╝╚═╚═╝  ╚═══╝  ╚═╝           
                                                       
██████╗████████████████╗██████╗███╗   ███████████████╗ 
██╔══████╔════██╔════████╔════╝████╗  ████╔════██╔══██╗
██║  ███████╗ ███████████║  █████╔██╗ ███████╗ ██████╔╝
██║  ████╔══╝ ╚════██████║   ████║╚██╗████╔══╝ ██╔══██╗
██████╔████████████████╚██████╔██║ ╚█████████████║  ██║
╚═════╝╚══════╚══════╚═╝╚═════╝╚═╝  ╚═══╚══════╚═╝  ╚═╝
                                                       
    """)

    while True:
        print()
        print("Choose an option:")
        print("1) Lap joint design.")
        print("2) Single cover butt joint design.")
        print("3) Double cover butt joint design.")
        print("0) Exit.")

        try:
            option = int(input("Choice: "))
        except KeyboardInterrupt:
            print("\nBye..")
            exit(0)
        except:
            continue

        if option in range(4):
            if option == 0:
                exit(0)
            elif option == 1:
                design_vals = lap()
                display_results(design_vals)
            elif option == 2:
                design_vals = scb()
                display_results(design_vals)
            elif option == 3:
                design_vals = dcb()
                display_results(design_vals)

        input("Press any key to continue....")

if __name__ == "__main__":
    main()
