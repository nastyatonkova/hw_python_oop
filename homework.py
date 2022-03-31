from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Informational message about training.

    Class properties:
    training_type -- class name of training
    duration -- duration of training (h)
    distance -- distance covered during training (km)
    speed -- avg speed during training (km/h)
    calories -- spent calories during training
    """

    #  message string with output of training
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.'
                              )
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Return formated training info message."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Base class of training.

    Constants:
    LEN_STEP -- distance covered by sportsmen in one step (m)
    M_IN_KM -- constant turning meters in kilometrs
    MIN_IN_HOUR -- minutes in hour

    Class properties:
    action -- number of actions (steps or padles)
    duration -- duration of training (h)
    weight -- weight of sportsman (kg)
    """

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Distance covered by sportsman during training (km)."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Return mean speed of movement during training (km/h)."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Return amount of calories during training."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return informational message about done training."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Training: run.

    Constants:
    RUN_COEFF_CAL_1 -- constant coefficient for calculating calories
    RUN_COEFF_CAL_2 -- constant coefficient for calculating calories

    Class properties:
    action -- number of actions (steps or padles)
    duration -- duration of training (h)
    weight -- weight of sportsman (kg)
    """

    RUN_COEFF_CAL_1: float = 18
    RUN_COEFF_CAL_2: float = 20

    # return amount of calories spent during running
    def get_spent_calories(self) -> float:
        """Return amount of calories while running."""
        return ((self.RUN_COEFF_CAL_1 * self.get_mean_speed()
                - self.RUN_COEFF_CAL_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Training: sports walking.

    Constants:
    WLK_COEFF_CAL_1 -- constant coefficient for calculating calories
    WLK_COEFF_CAL_2 -- constant coefficient for calculating calories

    Class properties:
    action -- number of actions (steps or padles)
    duration -- duration of training (h)
    weight -- weight of sportsman (kg)
    height -- heigh of sportsman (cm)
    """

    WLK_COEFF_CAL_1: float = 0.035
    WLK_COEFF_CAL_2: float = 0.029

    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Return amount of calories while sports walking."""
        return ((self.WLK_COEFF_CAL_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WLK_COEFF_CAL_2 * self.weight) * self.duration
                * self.MIN_IN_HOUR)


class Swimming(Training):
    """Training: swimming.

    Constants:
    LEN_STEP -- distance covered by sportsman with one padle during swimming
    SWM_COEFF_CAL_1 -- constant coefficient for calculating calories
    SWM_COEFF_CAL_2 -- constant coefficient for calculating calories

    Class properties:
    action -- number of actions (steps or padles)
    duration -- duration of training (h)
    weight -- weight of sportsman (kg)
    length_pool -- lenght of swimming pool (m)
    count_pool -- number of swim laps made by sportsman
    """

    LEN_STEP: float = 1.38
    SWM_COEFF_CAL_1: float = 1.1
    SWM_COEFF_CAL_2: float = 2

    def __init__(self, action, duration, weight,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Return mean speed while swimming (km/h)."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Return amount of calories while swimming."""
        return ((self.get_mean_speed() + self.SWM_COEFF_CAL_1)
                * self.SWM_COEFF_CAL_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Read data from sensors."""
    #  define dict with workout_type and corresponding training class
    workout_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    #  define class name
    cls_name = workout_dict[workout_type]
    #  create instance of training class
    training = cls_name(*data)
    return training


def main(training: Training) -> None:
    """Main function."""
    # create object info type InfoMessage
    info = training.show_training_info()
    training_message: str = info.get_message()
    print(training_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
