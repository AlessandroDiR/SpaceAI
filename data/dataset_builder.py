import json
import shutil
from types import SimpleNamespace
import jsonschema
import pandas as pd
from phrases_generator import PhrasesGenerator
from pathlib import Path
import sys

class DatasetBuilder():

    out_path: Path # destinazione dell'output
    train_path: Path
    test_path: Path
    validation_path: Path
    te_objects: int
    va_objects: int
    tr_objects: int

    def __init__(self, cfg: object) -> None:
        is_valid_path_err = self.__is_valid_path(Path(cfg.io.out_folder))
        if (is_valid_path_err is not None):
            print(is_valid_path_err)
            sys.exit(-1)

        self.out_path = Path(cfg.io.out_folder)

        self.train_path = self.out_path / "train"
        self.train_path.mkdir()

        self.test_path = self.out_path / "test"
        self.test_path.mkdir()
        
        self.validation_path = self.out_path / "validation"
        self.validation_path.mkdir()

        self.te_objects = int(cfg.synth_generator.total_objects * cfg.synth_generator.test_percentage)
        self.va_objects = int(cfg.synth_generator.total_objects * cfg.synth_generator.validation_percentage)
        self.tr_objects = cfg.synth_generator.total_objects - self.va_objects - self.te_objects

    def __is_valid_path(self, out_path: str):
        path = Path(out_path)
        if path.exists():
            # Se il percorso specificato non è una cartella valida, esco
            if not path.is_dir():
                return f"Directory \"{path.as_posix()}\" is not valid."
            
            # Se ha del contenuto, lo rimuovo.
            if not next(path.iterdir(), None) is None:
                shutil.rmtree(path)

        path.mkdir(exist_ok=True)

    def build(self):
        prefixes = ["train", "validation", "test"]
        paths = [self.train_path, self.validation_path, self.test_path]
        counts = [self.tr_objects, self.va_objects, self.te_objects]

        for prefix, path, count in zip(prefixes, paths, counts):
            filename = f"{path/prefix}.csv"
            generator = PhrasesGenerator(count)
            ins, outs = generator.run()
            data = [{"Input": i, "Action": o["action"], "Asset": o["asset"], "Start": o["start"], "End": o["end"]} for i, o in zip(ins, outs)]
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)

            print(f"DONE! {prefix} data saved into {Path(filename).resolve()}")


if __name__ == "__main__":
    cfg_file, schema_file = Path("../config/config.json"), Path("../config/config_schema.json")

    valid_input = cfg_file.is_file() and schema_file.is_file() and cfg_file.suffix == '.json' and schema_file.suffix == '.json'
 
    if valid_input:
        
        # Apro i due file e controllo se il json segue lo schema.           
        with open(Path(cfg_file)) as d:
            with open(Path(schema_file)) as s:

                # Carico i due json e utilizzo lo schema per validare il file di configurazione.
                data, schema = json.load(d), json.load(s)
                
                try:
                    # Il json 'data' è corretto secondo le regole di 'schema'?
                    jsonschema.validate(instance=data, schema=schema)                    
                except jsonschema.exceptions.ValidationError:
                    print(f'Json config file is not following schema rules.')
                    sys.exit(-1)
                except jsonschema.exceptions.SchemaError:
                    print(f'Json config schema file is invalid.')
                    sys.exit(-1)

    with open(Path(cfg_file)) as d:    
        builder = DatasetBuilder(json.loads(d.read(), object_hook=lambda d: SimpleNamespace(**d)))
        builder.build()     

