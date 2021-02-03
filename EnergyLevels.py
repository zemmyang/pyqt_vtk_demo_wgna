import math as m
import scipy.constants as const


JOULE_TO_MILLIKELVIN_CONV = 1/(const.Boltzmann*1e-3)
JOULE_TO_MICROKELVIN_CONV = 1/(const.Boltzmann*1e-6)
JOULE_TO_NANOKELVIN_CONV = 1/(const.Boltzmann*1e-9)


class QuantumHarmonicOscillator:
    def __init__(self, angular_frequency: float, potential_minimum=0.0, potential_barrier=m.inf):
        """
        :param angular_frequency: should be in Hz
        :param potential_minimum: should be in J
        :param potential_barrier: should be in J
        """
        self.angular_frequency = angular_frequency
        self.potential_minimum = potential_minimum
        self.potential_barrier = potential_barrier

        self.ground_state_energy = (0.5 * const.hbar * self.angular_frequency)

        self.energy_level_array = []
        if (self.ground_state_energy + potential_minimum) > self.potential_barrier:
            # bad case / too shallow / has holes = when the barrier is below the ground state
            self.energy_level_array.append(m.nan)
            self.number_of_energy_levels = 0
        else:
            _, self.number_of_energy_levels = self.calculate_number_of_energy_levels()

        # flags for units
        self.in_mk = False
        self.simplified = False

    def calculate_number_of_energy_levels(self):
        finite_energy_levels = 0
        _energy = self.ground_state_energy + self.potential_minimum
        self.energy_level_array.append(_energy)

        while _energy < self.potential_barrier:
            # this code does not considering the = case because it's too precise/floating point error
            finite_energy_levels += 1
            _energy = (const.hbar * self.angular_frequency * (finite_energy_levels + 0.5)) + self.potential_minimum
            if _energy < self.potential_barrier:
                self.energy_level_array.append(_energy)

        return self.energy_level_array, finite_energy_levels

    def convert_to_millikelvin(self):
        """ converts the units of energy levels to mK """
        self.in_mk = True
        self.energy_level_array = list(set([i*JOULE_TO_MILLIKELVIN_CONV
                                            for i in self.energy_level_array]))
        self.potential_minimum = self.potential_minimum*JOULE_TO_MILLIKELVIN_CONV
        self.ground_state_energy = self.ground_state_energy*JOULE_TO_MILLIKELVIN_CONV

    def simplify(self):
        """ rounds to 2 decimal places in mK """
        if not self.in_mk:
            self.convert_to_millikelvin()
            self.in_mk = True
        self.energy_level_array = [round(i, ndigits=2) for i in self.energy_level_array]
        self.potential_minimum = round(self.potential_minimum, ndigits=2)
        self.ground_state_energy = round(self.ground_state_energy, ndigits=2)
        self.simplified = True

    @classmethod
    def simplified_input(cls, angular_frequency: float, potential_minimum=0.0, potential_barrier=m.inf):
        """
        accepts input in simplified units
        :param angular_frequency: should be in MHz
        :param potential_minimum: should be in mK
        :param potential_barrier: should be in mK
        """
        cls.in_mk = True
        cls.simplified = True
        return cls(angular_frequency*1e6, potential_minimum*const.Boltzmann*1e-3, potential_barrier*const.Boltzmann*1e-3)


def testing():
    # data from the paper
    toroid_omega_z = 2.206734689921528e+07*2*const.pi
    toroid_u_min = -1.986212903395272e-25
    toroid_barrier = -10*const.Boltzmann*1e-3

    test = QuantumHarmonicOscillator(toroid_omega_z, potential_minimum=toroid_u_min, potential_barrier=toroid_barrier)
    test.simplify()

    print(toroid_u_min*JOULE_TO_MILLIKELVIN_CONV)
    print(test.ground_state_energy + test.potential_minimum)
    print(test.energy_level_array)
    print(test.number_of_energy_levels)


if __name__ == "__main__":
    testing()
