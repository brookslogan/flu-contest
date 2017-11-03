"""
===============
=== Purpose ===
===============

Creates submissions for Epicast and Archefilter.


=================
=== Changelog ===
=================

2016-11-29
  - not using default probability floor of 0.001 (must be provided)
2016-10-27
  - removed archefilter
  * updated for 2016 flu contest
2015-12-14
  * original version (combines make_epicast_submission.py and driver.py)
"""

# built-in
# external
# local
from epidate import EpiDate
#from fc_archefilter import Archefilter
from fc_baseline import Baseline
from fc_epicast import Epicast
from fc_hybrid import Hybrid
from forecast_io import ForecastIO


SEASON = 2017


class Submissions:

  def __init__(self, locations, num_backfill_samples=10000):
    self.past = Baseline(SEASON, locations, num_backfill_samples)

  def run_epicast(self, epiweek, min_week_prob, min_wili_prob):
    future = Epicast(SEASON, self.past.locations, verbose=True)
    forecaster = Hybrid('delphi-epicast', self.past, future)
    forecaster.min_week_prob = min_week_prob
    forecaster.min_wili_prob = min_wili_prob
    forecaster.smooth_weeks_bw = 0
    forecaster.smooth_wili_bw = 0
    forecaster.forecast_weeks = None
    forecaster.forecast_wili = None

    def update_epicast_df():
      forecaster.forecast_weeks = Epicast.get_week_forecast(future._num_users)
      forecaster.forecast_wili = Epicast.get_wili_forecast(future._num_users)
      #print('Updated Epicast df for %d users.' % future._num_users)
    forecaster._callback = update_epicast_df

    print('Generating epicast for', epiweek)
    forecaster.open()
    forecast = forecaster.forecast(epiweek)
    filename = ForecastIO.save_csv(forecast)
    forecaster.close()
    print(filename)
    return filename

  def run_archefilter(self, epiweek, min_week_prob, min_wili_prob, num_samples=10000):
    future = Archefilter(SEASON, self.past.locations, num_samples)
    forecaster = Hybrid('delphi-archefilter', self.past, future)
    forecaster.min_week_prob = min_week_prob
    forecaster.min_wili_prob = min_wili_prob
    forecaster.smooth_weeks_bw = 1
    forecaster.smooth_wili_bw = 1

    print('Generating archefilter for', epiweek)
    forecaster.open()
    forecast = forecaster.forecast(epiweek)
    filename = ForecastIO.save_csv(forecast)
    forecaster.close()
    print(filename)
    return filename


if __name__ == '__main__':
  epiweek = EpiDate.today().add_weeks(-2).get_ew()
  print('WARNING: For testing only!')
  print(' - Using very small number of samples')
  print(' - Not uploading submissions to database')
  print(' - Not emailing submissions to CDC')
  print(' - Assuming last published wILI on %d' % epiweek)
  print(' - Limited locations')

  sub = Submissions(['nat', 'hhs5', 'pa'], 1000)
  ec, af = None, None
  ec = sub.run_epicast(epiweek, 0.001, 0.001)
  #af = sub.run_archefilter(epiweek, 0.002, 0.002, num_samples=1000)

  print('Finished! Files are:')
  print(' -', ec)
  print(' -', af)
