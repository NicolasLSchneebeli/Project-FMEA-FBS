print('Please select from which component and attribute do you wish to create a condition:')
        comp_cond =[attributes[index].component.name for index in rep_cond]
        print(f'For {attrcond} there are:{comp_cond} ')
        inp_cond= input('Select which component name do you wish: ').lower()
        while inp_cond not in comp_names:
            print("Component not found")
            inp_comp2= input('Select which component name do you wish: ').lower()