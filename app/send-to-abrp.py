    def call(self, car: Car, ext_temp: float = None):
        try:
            if self.token is None or len(self.token) == 0:
                logger.debug("No abrp token provided")
            elif car.vin in self.abrp_enable_vin:
                energy = car.status.get_energy('Electric')

                if energy.level is None:
                    logger.debug("No energy level available")
                    return False

                tlm = {"utc": int(datetime.timestamp(energy.updated_at)),
                       "soc": energy.level,
                       "speed": getattr(car.status.kinetic, "speed", None),
                       "car_model": car.get_abrp_name(),
                       "current": car.status.battery.current,
                       "is_charging": energy.charging.status == "InProgress",
                       "lat": car.status.last_position.geometry.coordinates[1],
                       "lon": car.status.last_position.geometry.coordinates[0],
                       "power": energy.consumption
                       }
                if ext_temp is not None:
                    tlm["ext_temp"] = ext_temp
                params = {"tlm": json.dumps(tlm), "token": self.token, "api_key": self.api_key}
                response = requests.request("POST", self.url, params=params, proxies=self.proxies,
                                            verify=self.proxies is None, timeout=TIMEOUT_IN_S)
