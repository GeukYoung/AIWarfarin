import numpy as np
import math
from .apps import WarfarinConfig

# Create your views here.
def CalcWarfarin(sex, age, bwt, ht, PTINR_1, PTINR_2, PTINR_3, PTINR_4, WFR_1, WFR_2, WFR_3):
    sex_avg = 0.48489738
    sex_std = 0.4997719
    age_avg = 63.185894
    age_std = 15.272942
    bwt_avg = 60.84652
    bwt_std = 12.249503
    ht_avg = 161.60027
    ht_std = 9.54036
    BSA_avg = 1.6464512
    BSA_std = 0.1964058
    PTINR_avg = 1.8547587
    PTINR_std = 0.5918441
    WFR_avg = 2.934685
    WFR_std = 1.4178033
    data = []
    # Normalization function
    def norm(data, mean, std):
        result = (data - mean) / std
        return result
    # Denormalization function
    def denorm(data, mean, std):
        result = (data * std) + mean
        return result
    # (optional) Load model from a h5 file
    # Get the directory of the current script
    # current_dir = os.path.dirname(os.path.realpath(__file__))

    # # Name of your model file
    # model_name = "model_20200228-02.h5"

    # # Construct the full path to the model
    # model_path = os.path.join(current_dir, model_name)

    # # Load the model
    # model = load_model(model_path)

    # model = load_model("C:/Users/SNUBH/Downloads/model_20200228-02.h5")
    model = WarfarinConfig.model
    
    # Baseline values
    WFR_min = 0.5
    WFR_max = 8
    WFR_increment = 0.5
    WFR_dose_range = list(np.arange(WFR_min, (WFR_max+0.5), WFR_increment))
    # Manual input of sex, age, bwt and height
    # sex = float(input("Patient sex (Man=1, Woman=0): "))
    sex_norm = norm(sex, sex_avg, sex_std)
    # age = float(input("Patient age (years): "))
    age_norm = norm(age, age_avg, age_std)
    # bwt = float(input("Body weight (kg): "))
    bwt_norm = norm(bwt, bwt_avg, bwt_std)
    # ht = float(input("height (cm): "))
    ht_norm = norm(ht, ht_avg, ht_std)
    BSA = math.sqrt(bwt * ht / 3600)
    BSA_norm = norm(BSA, BSA_avg, BSA_std)
    # Manual input of PT INRs and warfarin doses
    # PTINR_1 = float(input("Day #1 PT INR: "))
    PTINR_1_norm = norm(PTINR_1, PTINR_avg, PTINR_std)
    #WFR_1 = float(input("Day #1 Warfarin dose (mg): "))
    WFR_1_norm = norm(WFR_1, WFR_avg, WFR_std)
    #PTINR_2 = float(input("Day #2 PT INR: "))
    PTINR_2_norm = norm(PTINR_2, PTINR_avg, PTINR_std)
    #WFR_2 = float(input("Day #2 Warfarin dose (mg): "))
    WFR_2_norm = norm(WFR_2, WFR_avg, WFR_std)
    #PTINR_3 = float(input("Day #3 PT INR: "))
    PTINR_3_norm = norm(PTINR_3, PTINR_avg, PTINR_std)
    #WFR_3 = float(input("Day #3 Warfarin dose (mg): "))
    WFR_3_norm = norm(WFR_3, WFR_avg, WFR_std)
    #PTINR_4 = float(input("Day #4 PT INR: "))
    PTINR_4_norm = norm(PTINR_4, PTINR_avg, PTINR_std)
    print("\n")
    # Initial data preparation: np array formation
    data3_imsi = np.array([sex_norm, age_norm, bwt_norm, ht_norm, BSA_norm]).reshape(1, 5)
    data4_imsi = np.array([[PTINR_1_norm, WFR_1_norm],
                        [PTINR_2_norm, WFR_2_norm],
                        [PTINR_3_norm, WFR_3_norm],
                        [PTINR_4_norm, 0]])
    data4 = data4_imsi.reshape(1, 4, 2)
    for dose in WFR_dose_range:
        # Virtual warfarin dose normalization
        dose_norm = norm(dose, WFR_avg, WFR_std)
        # data3 (sex, age, bwt, ht, BSA) reshaping to have proper shape
        # Data reorganization for PTINR Day #6 prediction.
        # Here, the last day PTINR is previously predicted PTINR day #5,
        # and warfarin dose is 'VIRTUAL'.
        data4_for_day05 = np.array([[data4[0, 0, 0], data4[0, 0, 1]],
                                    [data4[0, 1, 0], data4[0, 1, 1]],
                                    [data4[0, 2, 0], data4[0, 2, 1]],
                                    [data4[0, 3, 0], dose_norm]], dtype=np.float32)
        # data4 (PTINRs and WFRs) reshaping to have proper shape
        data4_for_day05 = data4_for_day05.reshape(1, 4, 2)
        # Prediction of PTINR day #5
        prediction_day05 = model.predict([data3_imsi, data4_for_day05])
        prediction_day05 = prediction_day05.squeeze()
        data4_for_day06 = np.array([[data4[0, 1, 0], data4[0, 2, 1]],
                                    [data4[0, 2, 0], data4[0, 3, 1]],
                                    [data4[0, 3, 0], dose_norm],
                                    [prediction_day05, dose_norm]], dtype=np.float32)
        data4_for_day06 = data4_for_day06.reshape(1, 4, 2)
        prediction_day06 = model.predict([data3_imsi, data4_for_day06])
        prediction_day06 = prediction_day06.squeeze()
        data4_for_day07 = np.array([[data4[0, 2, 0], data4[0, 3, 1]],
                                    [data4[0, 3, 0], dose_norm],
                                    [prediction_day05, dose_norm],
                                    [prediction_day06, dose_norm]], dtype=np.float32)
        data4_for_day07 = data4_for_day07.reshape(1, 4, 2)
        prediction_day07 = model.predict([data3_imsi, data4_for_day07])
        prediction_day07 = prediction_day07.squeeze()
        data4_for_day08 = np.array([[data4[0, 3, 0], dose_norm],
                                    [prediction_day05, dose_norm],
                                    [prediction_day06, dose_norm],
                                    [prediction_day07, dose_norm]], dtype=np.float32)
        data4_for_day08 = data4_for_day08.reshape(1, 4, 2)
        prediction_day08 = model.predict([data3_imsi, data4_for_day08])
        prediction_day08 = prediction_day08.squeeze()
        data4_for_day09 = np.array([[prediction_day05, dose_norm],
                                    [prediction_day06, dose_norm],
                                    [prediction_day07, dose_norm],
                                    [prediction_day08, dose_norm]], dtype=np.float32)
        data4_for_day09 = data4_for_day09.reshape(1, 4, 2)
        prediction_day09 = model.predict([data3_imsi, data4_for_day09])
        prediction_day09 = prediction_day09.squeeze()
        data4_for_day10 = np.array([[prediction_day06, dose_norm],
                                    [prediction_day07, dose_norm],
                                    [prediction_day08, dose_norm],
                                    [prediction_day09, dose_norm]], dtype=np.float32)
        data4_for_day10 = data4_for_day10.reshape(1, 4, 2)
        prediction_day10 = model.predict([data3_imsi, data4_for_day10])
        prediction_day10 = prediction_day10.squeeze()
        data4_for_day11 = np.array([[prediction_day07, dose_norm],
                                    [prediction_day08, dose_norm],
                                    [prediction_day09, dose_norm],
                                    [prediction_day10, dose_norm]], dtype=np.float32)
        data4_for_day11 = data4_for_day11.reshape(1, 4, 2)
        prediction_day11 = model.predict([data3_imsi, data4_for_day11])
        prediction_day11 = prediction_day11.squeeze()
        data4_for_day12 = np.array([[prediction_day08, dose_norm],
                                    [prediction_day09, dose_norm],
                                    [prediction_day10, dose_norm],
                                    [prediction_day11, dose_norm]], dtype=np.float32)
        data4_for_day12 = data4_for_day12.reshape(1, 4, 2)
        prediction_day12 = model.predict([data3_imsi, data4_for_day12])
        prediction_day12 = prediction_day12.squeeze()
        data4_for_day13 = np.array([[prediction_day09, dose_norm],
                                    [prediction_day10, dose_norm],
                                    [prediction_day11, dose_norm],
                                    [prediction_day12, dose_norm]], dtype=np.float32)
        data4_for_day13 = data4_for_day10.reshape(1, 4, 2)
        prediction_day13 = model.predict([data3_imsi, data4_for_day13])
        prediction_day13 = prediction_day13.squeeze()
        # PTINR day #5 denormalization
        # Collecting PTINRs of Day #5 to #13
        prediction_collected = np.array([prediction_day05, prediction_day06, prediction_day07,
                                        prediction_day08, prediction_day09, prediction_day10,
                                        prediction_day11, prediction_day12, prediction_day13])
        # Denormalization of predicted PTINRs
        prediction_collected_denorm = denorm(prediction_collected, PTINR_avg, PTINR_std)
        # Rounding up with 2 decimals and squeezing: (5, 1, 1) to (5,)
        prediction_collected_for_display = np.around(prediction_collected_denorm, decimals=2).squeeze()
        print("for continued dose of warfarin %.1f mg, predicted PTINRs for day 5 to 13 are:" % dose)
        print(prediction_collected_for_display, "\n")
        
        if dose == WFR_dose_range[0]:
            result_array = prediction_collected_for_display
        else:
            result_array = np.vstack((result_array, prediction_collected_for_display))
            
    print(result_array, "\n")
    return result_array