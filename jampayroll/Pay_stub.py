def currency_f0rmatter(number):
        """ FORMATS INTEGERS TO CURRENCY FORMAT, RETURNS STRING OBJ """
        res = '$ {:,.2f}'.format(number)
        return res

class Employee_form_data():
    """ A DUMMY PARTIAL CLASS ONLY TO CONTAIN INFO FROM EMPLOYEE
    -Employee(db.model) may be diff to inh- """
    def __init__(
        self,
        firstName='Selcuk',
        middleName='Attila',
        lastName='Turkoz',
        companyName='JAM Payroll',
        allowance=1,
        hourlyRate=44,
        hoursWorked= 80
        ):
        pass
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.companyName = companyName
        self.allowance = allowance
        self.hourlyRate = hourlyRate
        self.hoursWorked = hoursWorked

    def __str__(self):
        pass
        msg = 'never gonna keep me down'
        return msg

class ModGeneratedPayStubFrom(Employee_form_data):
    def __init__(self, payCntYr2Dt = 2, dateStart = '8/12/2019', dateEnd = '8/25/2019',*args, **kwargs):
        super(ModGeneratedPayStubFrom, self).__init__(*args, **kwargs)
        self.payCntYr2Dt = payCntYr2Dt
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.allowance_regression_slope = -0.1067
        self.allowance_regression_intcpt = 2.0444 
        self.allowanceFactor = float(self.allowance_regression_slope * self.allowance) +  self.allowance_regression_intcpt
        self.current = self.hoursWorked * self.hourlyRate
        self.curr3nt = self.hoursWorked * self.hourlyRate
        self.year2date = payCntYr2Dt * self.current
        self.hourlyR4te = self.hourlyRate
        self.year2d4te = self.year2date
        self.social_security = self.current * self.allowanceFactor *9.3/150
        self.social_security_perc = self.allowanceFactor *9.3/150*100
        self.social_security_year2date = self.current *  self.allowanceFactor *9.3 / 150 * payCntYr2Dt
        self.medicare = self.current *  self.allowanceFactor *2.18 / 150
        self.medicare_perc = self.allowanceFactor *2.18 / 150*100
        self.medicare_year2date = self.current * 2.18 / 150 *  self.allowanceFactor *payCntYr2Dt
        self.futa = self.current * 0.90 * self.allowanceFactor / 150
        self.futa_perc = 0.90 * self.allowanceFactor / 150*100
        self.futa_year2date = self.current * 0.90 / 150 *  self.allowanceFactor *payCntYr2Dt
        self.co_unemp = self.current * self.allowanceFactor * 1.77 / 150
        self.co_unemp_perc = self.allowanceFactor * 1.77 / 150*100
        self.co_unemp_year2date = self.current * 1.77 / 150 * payCntYr2Dt * self.allowanceFactor 
        self.taxes = self.current * 11.48 / 150 * self.allowanceFactor
        self.taxes_perc = 11.48 / 150 * self.allowanceFactor *100 
        self.taxes_year2date = self.current * 11.48 / 150 * payCntYr2Dt * self.allowanceFactor
        self.net_pay = self.current*(1-(11.48/150*self.allowanceFactor))
        self.net_pay_perc = (1-(11.48/150*self.allowanceFactor))*100
        self.net_pay_y2d =  self.current*(1-(11.48/150*self.allowanceFactor))* payCntYr2Dt
    
    def dict_for_perc(self):
        pass
        dict = {
        'Social Security' : float(self.social_security_perc), 
        'Medicare' : float(self.medicare_perc), 
        'FUTA' : float(self.futa_perc), 
        'State Unemployment Tax' : float(self.co_unemp_perc), 
        'Taxes' : float(self.taxes_perc), 
        'Net Pay': float(self.net_pay_perc)
        }
        return dict


    def __str__(self):
        msg = 'never gonna keep me down'
        return msg

class Pay_stub(Employee_form_data):
    def __init__(self, pay_count_year2date = 2 ):
        pass
        self.pay_count_year2date = pay_count_year2date
        self.current = self.hoursWorked * self.hourlyRate
        self.year2date = pay_count_year2date * self.current
        self.hourlyRate = currency_f0rmatter(self.hourlyRate)
        self.curr3nt = currency_f0rmatter(self.current)
        self.year2d4te = currency_f0rmatter(self.year2date)
        self.social_security = currency_f0rmatter(self.current * 9.3/150)
        self.social_security_year2date = currency_f0rmatter(self.current * 9.3 / 150 * pay_count_year2date)
        self.medicare = currency_f0rmatter(self.current * 2.18 / 150)
        self.medicare_year2date = currency_f0rmatter(self.current * 2.18 / 150 * pay_count_year2date)
        self.futa = currency_f0rmatter(self.current * 0.90/ 150)
        self.futa_year2date = currency_f0rmatter(self.current * 0.90 / 150 * pay_count_year2date)
        self.co_unemp = currency_f0rmatter(self.current * 1.77 / 150)
        self.co_unemp_year2date = currency_f0rmatter(self.current * 1.77 / 150 * pay_count_year2date)
        self.taxes = currency_f0rmatter(self.current * 11.48 / 150)
        self.taxes_year2date = currency_f0rmatter(self.current * 11.48 / 150 * pay_count_year2date)
        self.net_pay = currency_f0rmatter(self.current * 138.52 / 150)
        self.net_pay_y2d = currency_f0rmatter(self.current * 138.52 / 150 * pay_count_year2date)
    
    def __str__(self):
        msg = 'I get knocked down but I get up again'
        return msg

if __name__ == "__main__":
    pass
