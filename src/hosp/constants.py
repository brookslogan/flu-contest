# all locations we can query
STATE_LIST = [
              'ga', 'or',
            #   'md', 'mi', 'mn', 
            #   'nm',  
            #   'oh', 'or', 
            #   'tn', 'ut',
              'network_all']
# descriptions for age groups 0-4
GROUP_DESCRIPTIONS = ['Ages 0-4', 'Ages 5-17', 'Ages 18-49', 
                    'Ages 50-64', 'Ages 65+']

# hyperparameters for machine learning models
RIDGE_ALPHA = 0.5
ESTIMATIORS, DEPTH = 50, 3
# hyperparameters for quantile models
UPPER_QUANT, MID_QUANT, LOWER_QUANT = 0.95, 0.5, 0.05
EPS = 0.05
# hyperparameters for 'all' mode in training
FIRST_YEAR, YEAR_WINDOW = 2012, 1
# hyperparameters for prediction
PENALTY = 0.03
