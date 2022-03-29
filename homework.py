from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Informational message about training."""
    #  class name of training
    training_type: str
    #  duration of training in hours
    duration: float
    #  distance covered during training in km
    distance: float
    #  avg speed during training
    speed: float
    #  spent calories during training
    calories: float
    #  message string with output of training
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Base class of training."""
    # distance covered by sportsmen in one step (m.)
    LEN_STEP: float = 0.65
    # constant turning meters in kilometrs
    M_IN_KM: float = 1000
    # minutes in hour
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 # number of actions (steps or padles)
                 action: int,
                 # duration of training (hours)
                 duration: float,
                 # weight of sportsman (kilogramms)
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    # return distance covered by sportsman during training (km.)
    def get_distance(self) -> float:
        """Become distance in kilometrs."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    # return mean speed of movement during training (km/h)
    def get_mean_speed(self) -> float:
        """Return mean speed of movement."""
        return self.get_distance() / self.duration

    # return amount of calories spent during training
    def get_spent_calories(self) -> float:
        """Return amount of calories."""
        pass

    # return object type class InfoMessage
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
    """Training: run."""
    RUN_COEFF_CAL_1: float = 18
    RUN_COEFF_CAL_2: float = 20

    def __init__(self,
                 # number of actions (steps)
                 action: int,
                 # duration of training (hours)
                 duration: float,
                 # weight of sportsman (kilogramms)
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    # return amount of calories spent during running
    def get_spent_calories(self) -> float:
        """Return amount of calories while running."""
        return ((self.RUN_COEFF_CAL_1 * self.get_mean_speed()
                - self.RUN_COEFF_CAL_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Training: sports walking."""
    WLK_COEFF_CAL_1: float = 0.035
    WLK_COEFF_CAL_2: float = 0.029

    def __init__(self,
                 # nubmer of actions (steps)
                 action: int,
                 # duration of training (hours)
                 duration: float,
                 # weight of sportsman (kilogramms)
                 weight: float,
                 # height of sportsman (centimetrs)
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    # return amount of calories spent during sports walking
    def get_spent_calories(self) -> float:
        """Return amount of calories while sports walking."""
        return ((self.WLK_COEFF_CAL_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WLK_COEFF_CAL_2 * self.weight) * self.duration
                * self.MIN_IN_HOUR)


class Swimming(Training):
    # distance covered by sportsman with one padle during swimming
    LEN_STEP: float = 1.38
    SWM_COEFF_CAL_1: float = 1.1
    SWM_COEFF_CAL_2: float = 2
    """Training: swimming."""
    def __init__(self,
                 # nubmer of actions (padles)
                 action: int,
                 # duration of training (hours)
                 duration: float,
                 # weight of sportsman (kilogramms)
                 weight: float,
                 # lenght of swimming pool (meters)
                 length_pool: int,
                 # number of swim laps made by sportsman
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    # return mean speed of movement during training (km/h)
    def get_mean_speed(self) -> float:
        """Return mean speed while swimming."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    # return amount of calories spent during sports swimming
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
