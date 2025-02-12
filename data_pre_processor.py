class DataPreProcessor:
    @staticmethod
    def process_shaker_data(row):
        vpn = str(row['VPN']).lower()
        alt_vpn = str(row['alt-VPN']).lower()
        primary_name = row['Primary Name']
        notes = row.get('Notes', '')
        eta = row.get('ETA', '')
        return vpn, alt_vpn, primary_name, notes, eta

    @staticmethod
    def process_downloader_data(row):
        primary_name = row['Primary Name']
        url = row['URL']
        file_type = row['Type']
        return primary_name, url, file_type

    def prepare_data(self, data, process_type):
        processors = {
            'shaker': self._prepare_shaker_data,
            'download': self._prepare_downloader_data
        }
        
        processor = processors.get(process_type)
        if not processor:
            raise ValueError(f"Unknown process type: {process_type}")
        
        return processor(data)

    def _prepare_shaker_data(self, data):
        prepared_data = []
        for row in data:
            row_data = self.process_shaker_data(row)
            if not row_data[0]:  # Skip if VPN is empty
                print("Skipping row with blank VPN value.")
                continue
            prepared_data.append(row_data)
        return prepared_data

    def _prepare_downloader_data(self, data):
        return [self.process_downloader_data(row) for row in data]