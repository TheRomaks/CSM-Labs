def run_analytical(lambda_rate, service_time):
    try:
        ro = lambda_rate * service_time
        p0 = 1 / (1 + ro)
        p_otkaza = ro / (1 + ro)
        q = 1 - p_otkaza
        A = lambda_rate * q
        return {"ro": ro, "p0": p0, "p_otkaza": p_otkaza, "q": q, "A": A}
    except Exception as e:
        raise RuntimeError("Ошибка при аналитическом расчете: " + str(e))
