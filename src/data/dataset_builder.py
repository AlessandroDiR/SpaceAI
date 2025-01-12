import json
import shutil
from types import SimpleNamespace
import jsonschema
import pandas as pd
from pathlib import Path
import sys
from sentences_generator import SentencesGenerator

class DatasetBuilder():

    out_path: Path          # Destinazione dell'output
    tr_path: Path           # Destinazione dati train
    te_path: Path           # Destinazione dati test
    va_path: Path           # Destinazione dati validation

    tr_objects: int         # Totale oggetti per train
    te_objects: int         # Totale oggetti per test
    va_objects: int         # Totale oggetti per validazione

    tr_as_duration: bool | str
    te_as_duration: bool | str
    va_as_duration: bool | str

    def __init__(self, cfg: object) -> None:
        is_valid_path_err = self.__is_valid_path__(Path(cfg.io.out_folder))
        if (is_valid_path_err is not None):
            print(is_valid_path_err)
            sys.exit(-1)

        self.out_path = Path(cfg.io.out_folder)

        self.tr_path = self.out_path / "train"
        self.tr_path.mkdir()

        self.te_path = self.out_path / "test"
        self.te_path.mkdir()

        self.va_path = self.out_path / "validation"
        self.va_path.mkdir()

        self.te_objects = int(cfg.sentences_generator.total_objects * cfg.sentences_generator.test_percentage)
        self.va_objects = int(cfg.sentences_generator.total_objects * cfg.sentences_generator.validation_percentage)
        self.tr_objects = cfg.sentences_generator.total_objects - self.va_objects - self.te_objects

        self.tr_as_duration = cfg.sentences_generator.params.train.as_duration
        self.te_as_duration = cfg.sentences_generator.params.test.as_duration
        self.va_as_duration = cfg.sentences_generator.params.validation.as_duration


    def __is_valid_path__(self, out_path: str):
        """Validate specified path
        
        Args:\n
        out_path -- the out path to validate

        Returns:\n
        str -> the error message if the path is not valid\n
        None -> if the path pass all validations
        """
        path = Path(out_path)
        if path.exists():
            # Se il percorso specificato non è una cartella valida, esco
            if not path.is_dir():
                return f"Directory \"{path.as_posix()}\" is not valid."
            
            # Se ha del contenuto, lo rimuovo.
            if not next(path.iterdir(), None) is None:
                shutil.rmtree(path)

        path.mkdir(exist_ok=True)

    
    def info(self):
        print("-------------------------------------")
        print(f"{self.__class__.__name__} info")
        print("-------------------------------------")
        print("Subfolders to generate:")
        print(f"Path: {Path(self.tr_path.resolve())}")
        print(f"Path: {Path(self.te_path.resolve())}")
        print(f"Path: {Path(self.va_path.resolve())}")
        print("\nNumber of object to generate:")
        print("{cat:.<{width}}: {value}".format(cat="Train", width=15, value=self.tr_objects))
        print("{cat:.<{width}}: {value}".format(cat="Test", width=15, value=self.te_objects))
        print("{cat:.<{width}}: {value}".format(cat="Validation", width=15, value=self.va_objects))
        print("-------------------------------------")
        print("END info")
        print("-------------------------------------\n")


    def build(self):
        print("Builder running...")
        generator = SentencesGenerator(seed=42)
        train_data = (self.__build_data__(generator, self.tr_objects, self.tr_as_duration))
        test_data = (self.__build_data__(generator, self.te_objects, self.te_as_duration))
        valiation_data = (self.__build_data__(generator, self.va_objects, self.va_as_duration))

        data = [train_data, test_data, valiation_data]
        paths = [self.tr_path, self.te_path, self.va_path]
        prefixes = ["train", "test", "validation"]

        for data, path, prefix in zip(data, paths, prefixes):
            filename = f"{path/prefix}.csv"
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)

            print(f"DONE! {prefix} data saved into {Path(filename).resolve()}")
    
    def __build_data__(self, generator: SentencesGenerator, count: int, as_duration: bool | str):
        data = ()
        if as_duration == "mix":
            as_duration_count = count // 2
            as_range_count = count - as_duration_count
            ins_as_duration, outs_as_duration = generator.run(count=as_duration_count, datetime_as_duration=True)
            ins_as_range, outs_as_range = generator.run(count=as_range_count, datetime_as_duration=False)
            data = (ins_as_duration + ins_as_range, outs_as_duration + outs_as_range)
        elif as_duration:
            data = generator.run(count=count, datetime_as_duration=True)
        else:
            data = generator.run(count=count)

        ins, outs = data
        return [{"Input": i, "Asset": o["asset"], "Start": o["start"], "End": o["end"]} for i, o in zip(ins, outs)]


if __name__ == "__main__":
    cfg_file, schema_file = Path("../../config/config.json"), Path("../../config/config_schema.json")

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
        builder.info()
        builder.build()

