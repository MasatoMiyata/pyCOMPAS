//
//プログラム名：Midzon
//
//複数の開口を持つ単室の中性帯高さ(m)と出入の流量(m3/h)を算出する
//

namespace Midzon
{
    //開口に関するパラメータ値を保管するクラス
    class OpeningRelatedInputValueLib
    {
        private float _RK;   //流速係数(-)
        private float _DW;   //開口の幅(m)
        private float _DHL;  //開口の下端高さ(m)
        private float _DHU;  //開口の上端高さ(m)
        private float _WK;   //風圧係数(-)

        //コンストラクタ
        public OpeningRelatedInputValueLib()
        {
            this._RK = 0;
            this._DW = 0;
            this._DHL = 0;  
            this._DHU = 0;
            this._WK = 0;
        }

        //プロパティ設定群
        public float RK
        {
            get { return this._RK; }
        }

        public float DW
        {
            get { return this._DW; }
        }

        public float DHL
        {
            get { return this._DHL; }
        }

        public float DHU
        {
            get { return this._DHU; }
        }

        public float WK
        {
            get { return this._WK; }
        }

        //CSV文字列の内容を解析する
        public bool AnalyzeThisLine(String[] values)
        {
            //値の数が9個ない場合はエラーとする
            if (values.Length != 9)
                return false;

            //最初の5個目から9個目までの値を取り込む
            float fVal;
            if (float.TryParse(values[4], out fVal) == false)
                return false;
            this._RK = fVal;
            if (float.TryParse(values[5], out fVal) == false)
                return false;
            this._DW = fVal;
            if (float.TryParse(values[6], out fVal) == false)
                return false;
            this._DHL = fVal;
            if (float.TryParse(values[7], out fVal) == false)
                return false;
            this._DHU = fVal;
            if (float.TryParse(values[8], out fVal) == false)
                return false;
            this._WK = fVal;

            return true;
        }
    }

    //入力値を保管するクラス
    class InputValueLib
    {
        private float _TO;   //外気温度(℃)
        private float _TI;   //室内温度(℃)
        private float _VEL;  //外部風速(m/s)
        private int _K;      //開口の数
        private OpeningRelatedInputValueLib[]? opngRltdInputValueLibArray;
                            //開口に関連するパラメータの管理クラス配列

        //コンストラクタ
        public InputValueLib()
        {
            this._TO = 0;
            this._TI = 0;
            this._VEL = 0;
            this._K = 0;
            this.opngRltdInputValueLibArray = null;
        }

        //プロパティ設定群
        public float TO
        {
            get { return this._TO; }
        }

        public float TI
        {
            get { return this._TI; }
        }

        public float VEL
        {
            get { return this._VEL; }
        }

        public int K
        {
            get { return this._K; }
        }

        //1行目の内容を解析する
        //入力値：1行目のCSV文字列
        //出力値：解析でエラーがなければtrue、あればfalse
        private bool AnalyzeFirstLine(String valueLine)
        {
            //カンマで分割する
            String[] values = valueLine.Trim().Split(",");
            //値の数が9個ない場合はエラーとする
            if (values.Length != 9)
                return false;

            //最初の4個の値を取り込む
            float fVal;
            if (float.TryParse(values[0], out fVal) == false)
                return false;
            this._TO = fVal;
            if (float.TryParse(values[1], out fVal) == false)
                return false;
            this._TI = fVal;
            if (float.TryParse(values[2], out fVal) == false)
                return false;
            this._VEL = fVal;
            int nVal;
            if (int.TryParse(values[3], out nVal) == false)
                return false;
            this._K = nVal;

            //Kが1以上でない場合はエラーとする
            if (this._K <= 0)
                return false;

            //開口に関連するパラメータの管理クラスを生成する
            OpeningRelatedInputValueLib newLib = new OpeningRelatedInputValueLib();
            //CSV値文字列の内容を解析する
            bool result = newLib.AnalyzeThisLine(values);
            if (result == false)
                return false;
            //メンバー変数に管理クラスを追加する
            this.opngRltdInputValueLibArray = new OpeningRelatedInputValueLib[1];
            this.opngRltdInputValueLibArray[0] = newLib;

            return true;
        }

        //2行目以降の内容を解析する
        //入力値：解析対象となるCSV文字列と行インデックス
        //出力値：解析でエラーがなければtrue、あればfalse
        private bool AnalyzeThisLine(String valueLine, int index)
        {
            //カンマで分割する
            String[] values = valueLine.Trim().Split(",");
            //値の数が9個ない場合はエラーとする
            if (values.Length != 9)
                return false;

            //開口に関連するパラメータの管理クラスを生成する
            OpeningRelatedInputValueLib newLib = new OpeningRelatedInputValueLib();
            //CSV値文字列の内容を解析する
            bool result = newLib.AnalyzeThisLine(values);
            if (result == false)
                return false;
            //メンバー変数に管理クラスを追加する
            if (this.opngRltdInputValueLibArray == null)
                return false;
            Array.Resize(ref this.opngRltdInputValueLibArray
                        , this.opngRltdInputValueLibArray.Length + 1);
            this.opngRltdInputValueLibArray[
                this.opngRltdInputValueLibArray.Length - 1] = newLib;

            return true;
        }

        //CSVファイルからの入力値取得
        //入力値：ロード対象となるCSVファイルへのフルパス
        //出力値：ロードでエラーがなければtrue、あればfalse
        public bool LoadInputValues(String _CSVFilePath)
        {
            //指定したCSVファイルが存在しない場合はエラーとする
            if (System.IO.File.Exists(_CSVFilePath) == false)
                return false;

            //ファイル内容を取り込む
            StreamReader sr = new StreamReader(_CSVFilePath);
            String _CSV = sr.ReadToEnd();
            sr.Close();

            //改行で分割する
            String[] valueLines = _CSV.Split("\n");
            //3行以上ない場合はエラーとする
            if (valueLines.Length <= 2)
                return false;

            //CSV値文字列の1行目の内容を解析する
            bool result = AnalyzeFirstLine(valueLines[2]);
            if(result == false) 
                return false;
            //ロードした開口の数が不正の場合はエラーとする
            if (this._K <= 0)
                return false;

            //CSV値文字列の2行目以降を順次調べる
            for (int lineID = 3; lineID <= K + 1; lineID++)
            {
                //空行の場合はエラーとする
                if (valueLines[lineID] == "")
                    return false;

                result = AnalyzeThisLine(valueLines[lineID], lineID - 2);
                if (result == false)
                    return false;
            }

            return true;
        }

        //指定したインデックスの開口に関するパラメータ値を保管するクラスを取得する
        //入力値：取得したい要素のインデックス
        //出力値：指定したインデックスに対応するクラス要素
        //　　　　(インデックスが不正の場合はnullを返す)
        public OpeningRelatedInputValueLib? GetThisOpeningRelatedInputValueLib(int index)
        {
            if (this.opngRltdInputValueLibArray != null
                && index >= 0
                && index < this.opngRltdInputValueLibArray.Length)
                return this.opngRltdInputValueLibArray[index];
            else
                return null;
        }
    }

    //個々の開口に対する中性帯高さと出入の流量を保管するクラス
    class MidzonAndFlowRatePerOpeningLib
    {
        private float _GI;   //流入量(m3/h)
        private float _GO;   //流出量(m3/h)
        private float _DY;   //中性帯高さ(m)

        //デフォルトコンストラクタ
        public MidzonAndFlowRatePerOpeningLib()
        {
            this._GI = 0;
            this._GO = 0;
            this._DY = 0;
        }

        //初期値を引数として与えるコンストラクタ
        public MidzonAndFlowRatePerOpeningLib(float _GI, float _GO, float _DY)
        {
            this._GI = _GI;
            this._GO = _GO;
            this._DY = _DY;
        }

        //プロパティ設定群
        public float GI
        {
            get { return this._GI; }
        }

        public float GO
        {
            get { return this._GO; }
        }

        public float DY
        {
            get { return this._DY; }
        }

    }

    //すべての開口に対する中性帯高さと出入の流量を保管するクラス
    class MidzonAndFlowRateLib
    {
        private MidzonAndFlowRatePerOpeningLib[]? mdznAdFlwRtPrOpngArray;
                        //個々の開口に対する計算結果を保管するクラスの配列

        //コンストラクタ
        public MidzonAndFlowRateLib()
        {
            this.mdznAdFlwRtPrOpngArray = null;
        }

        //流入量を計算する
        //入力値：流量係数RK、開口の幅DW、中性帯高さYY
        //　　　　風による中性帯修正量DDY、開口部下端高さDHL
        //　　　　外気比重量RO、外気比重量と室内空気比重量の差DR
        //出力値：流入量
        private float CalculateInputFlowRate(float RK, float DW, float YY
                        , float DDY, float DHL, float RO, float DR)
        {
            double ret = 2.0 / 3.0 * RK * DW
                        * Math.Pow((YY + DDY) - DHL, 1.5) 
                        * Math.Sqrt(19.6 * RO * DR);

            return (float)ret;
        }

        //流出量を計算する
        //入力値：流量係数RK、開口の幅DW、開口部上端高さDHU
        //        中性帯高さYY、風による中性帯修正量DDY、
        //　　　　室内空気比重量RI、外気比重量と室内空気比重量の差DR
        //出力値：流入量
        private float CalculateOutputFlowRate(float RK, float DW, float DHU
                        , float YY, float DDY, float RI, float DR)
        {
            double ret = 2.0 / 3.0 * RK * DW
                        * Math.Pow(DHU - (YY + DDY), 1.5)
                        * Math.Sqrt(19.6 * RI * DR);

            return (float)ret;
        }

        //ローカル変数に計算結果を書き込む
        //入力値：入力値の組み合わせ数、流入量の配列、流出量の配列、中性帯高さの配列
        private void ApplyCalculationResult(int valueCount
                        , float[] GIValues, float[] GOValues, float[] DYValues
                        , float RO, float RI)
        {
            if (valueCount <= 0
                || RO == 0
                || RI == 0)
                return;
            if (GIValues.Length != valueCount
                || GOValues.Length != valueCount
                || DYValues.Length != valueCount)
                return;

            //計算結果を保管するクラスの配列を確保する
            this.mdznAdFlwRtPrOpngArray = new MidzonAndFlowRatePerOpeningLib[valueCount];
            for(int i = 0; i < valueCount; i++)
            {
                //計算結果を与えて新しい計算結果保管クラスを生成する
                MidzonAndFlowRatePerOpeningLib curResultValueLib 
                    = new MidzonAndFlowRatePerOpeningLib(
                            GIValues[i] / RO * 3600
                            , GOValues[i] / RI * 3600
                            , DYValues[i]);
                            //GIおよびGOについて、kg/secからm3/hへの単位変換を実施

                //メンバー変数に書き込む
                this.mdznAdFlwRtPrOpngArray[i] = curResultValueLib;
            }
        }

        //中性帯高さおよび出入の流量を計算する
        //入力値：CSVファイルから与えたパラメータ値
        //出力値：計算でエラーがなければtrue、あればfalse
        public bool Calculate(InputValueLib inputValueLib)
        {
            float RO = 353.2f / (273.0f + inputValueLib.TO);
            float RI = 353.2f / (273.0f + inputValueLib.TI);
            float DR = Math.Abs(RO - RI);

            float[] DDY = new float[inputValueLib.K];
                            //風による中性帯修正量
            for(int i = 0; i < inputValueLib.K; i++)
            {
                OpeningRelatedInputValueLib? curValueLib
                    = inputValueLib.GetThisOpeningRelatedInputValueLib(i);
                if (curValueLib == null)
                    return false;

                DDY[i] = (float)(curValueLib.WK * RO * Math.Pow(inputValueLib.VEL, 2)) / (19.6f * DR);

            }

            float[] DHL1 = new float[inputValueLib.K];
                            //開口の下端高さ
            float[] DHU1 = new float[inputValueLib.K];
                            //開口の上端高さ
            for (int i = 0; i < inputValueLib.K; i++)
            {
                OpeningRelatedInputValueLib? curValueLib
                    = inputValueLib.GetThisOpeningRelatedInputValueLib(i);
                if (curValueLib == null)
                    return false;

                if (DDY[i] != 0) {
                    DHL1[i] = curValueLib.DHL - DDY[i];
                    DHU1[i] = curValueLib.DHU - DDY[i];
                }
                else {
                    DHL1[i] = curValueLib.DHL;
                    DHU1[i] = curValueLib.DHU;
                }
            }

            float Y1 = DHL1[0];
            float Y2 = DHU1[0];

            for(int i = 0; i < inputValueLib.K; i++)
            {
                if (DHL1[i] > Y1) {
                    if (DHU1[i] < Y2) 
                        break;
                }
                if (DHL1[i] <= Y1) {
                    Y1 = DHL1[i];
                }
                Y2 = DHU1[i];
            }

            float J = 0;
            float[] GI = new float[inputValueLib.K];
                            //流入量
            float[] GO = new float[inputValueLib.K];
                            //流出量
            float[] DY = new float[inputValueLib.K];
                            //中性帯高さ

            do
            {
                float YY = (Y1 + Y2) * 0.5f;
                float TGI = 0.0f;
                float TGO = 0.0f;

                for (int i = 0; i < inputValueLib.K; i++)
                {
                    OpeningRelatedInputValueLib? curValueLib
                        = inputValueLib.GetThisOpeningRelatedInputValueLib(i);
                    if (curValueLib == null)
                        return false;

                    DY[i] = YY + DDY[i];
                    if (curValueLib.DHL < DY[i])
                    {
                        if (curValueLib.DHU > DY[i])
                        {
                            GI[i] = CalculateInputFlowRate(curValueLib.RK, curValueLib.DW
                                                , YY, DDY[i], curValueLib.DHL, RO, DR);
                            GO[i] = CalculateOutputFlowRate(curValueLib.RK, curValueLib.DW
                                                    , curValueLib.DHU, YY, DDY[i], RI, DR);
                        }
                        else
                        {
                            GI[i] = CalculateInputFlowRate(curValueLib.RK, curValueLib.DW
                                                , YY, DDY[i], curValueLib.DHL, RO, DR);
                            GO[i] = 0.0f;
                        }
                    }
                    else
                    {
                        GI[i] = 0.0f;
                        GO[i] = CalculateOutputFlowRate(curValueLib.RK, curValueLib.DW
                                                , curValueLib.DHU, YY, DDY[i], RI, DR);
                    }
                    TGI = TGI + GI[i];
                    TGO = TGO + GO[i];
                }
                if (TGI == TGO) 
                    break;

                //以下、流量収支の誤差判定を行う
                float GOSA = (TGI + TGO) * 0.005f;
                if ((Math.Abs(TGI - TGO)) < GOSA) 
                    break;
                J = J + 1;
                if (J == 100)
                {
                    for (int i = 0; i < inputValueLib.K; i++)
                        DY[i] = 0.0f;
                    break;
                }

                if (TGI > TGO)
                {
                    Y2 = YY;
                    continue;
                }
                Y1 = YY;
            } while (true);

            //ローカル変数に計算結果を書き込む
            ApplyCalculationResult(inputValueLib.K, GI, GO, DY, RO, RI);

            return true;
        }

        //計算結果の要素数を取得する
        //入力値：なし
        //出力値：要素数
        public int GetCalculationResultCount() {
            if (this.mdznAdFlwRtPrOpngArray != null)
                return this.mdznAdFlwRtPrOpngArray.Length;
            else
                return 0;
        }

        //指定したインデックスの計算結果を取得する
        //入力値：取得したい計算結果のインデックス
        //出力値：指定したインデックスの計算結果要素
        //          (インデックスが不正の場合はnullを返す)
        public MidzonAndFlowRatePerOpeningLib? GetThisCalculationResult(int index)
        {
            if (this.mdznAdFlwRtPrOpngArray != null
                && index >= 0
                && index < this.mdznAdFlwRtPrOpngArray.Length)
                return this.mdznAdFlwRtPrOpngArray[index];
            else
                return null;
        }
    }

    //計算結果をCSVファイルとして保存するクラス
    class SaveCalculationResultLib
    {
        //保存すべきCSV文字列を生成する
        //入力値：計算結果を保管するクラス
        //出力値：保存すべきCSV文字列
        private String GetCSVString(MidzonAndFlowRateLib mdznAdFlwRtLib)
        {
            //結果要素数を取得する
            int resultCount = mdznAdFlwRtLib.GetCalculationResultCount();

            //戻り値となるCSV文字列を保管するローカル変数
            String result = "Input Flow Rate GI(i)(m3/h),";
            result += "Output Flow Rate GO(i)(m3/h),";
            result += "Neutral Zone Height DY(m)";

            //すべての要素について処理する
            for (int i = 0; i < resultCount; i++) {
                //現在のインデックスに対応する結果要素を取得する
                MidzonAndFlowRatePerOpeningLib? curResultItem
                    = mdznAdFlwRtLib.GetThisCalculationResult(i);
                if (curResultItem == null)
                    continue;

                //現在のインデックスに対応するCSV文字列を生成する
                String curResult = curResultItem.GI.ToString() + "," 
                                    + curResultItem.GO.ToString() + ","
                                    + curResultItem.DY.ToString();
                //戻り値に追記する
                result = result + "\n" + curResult;
            }

            return result;
        }

        //計算結果をCSVファイルとして保存する
        //入力値：エクスポート先フォルダ名、計算結果を保管するクラス
        //出力値：エクスポートでエラーがなければtrue、あればfalse
        public bool Save(String exportFolder, MidzonAndFlowRateLib mdznAdFlwRtLib)
        {
            //保存すべきCSV文字列を生成する
            String _csvString = GetCSVString(mdznAdFlwRtLib);

            //保存ファイルへのパスを生成する
            String exportFilePath = exportFolder + "\\ResultValues.csv";
            //保存を実行する
            StreamWriter sw = new StreamWriter(exportFilePath, false
                                            , System.Text.Encoding.UTF8);
            sw.Write(_csvString);
            sw.Close();

            return true;
        }
    }

    //Main関数を保持するクラス
    internal class Program
    {
        //Main関数
        static void Main(string[] args)
        {
            //入力値を持つCSVファイルへのフルパスを取得する
            Console.WriteLine("Input CSV File Path?");
            String? _CSVFilePath = Console.ReadLine();
            if (_CSVFilePath == null)
                return;

            //CSVファイルから入力値をロードする
            InputValueLib inputValueLib = new InputValueLib();
            bool result = inputValueLib.LoadInputValues(_CSVFilePath);
            if (result == false)
            {
                Console.WriteLine("Error occured on input CSV loading");
                return;
            }

            //中性帯高さと出入の流量を計算する
            MidzonAndFlowRateLib mdznAdFlwRtLib = new MidzonAndFlowRateLib();
            result = mdznAdFlwRtLib.Calculate(inputValueLib);
            if (result == false)
            {
                Console.WriteLine("Error occured on midzon and flow rate calculation");
                return;
            }

            //入力CSVファイルが存在するフォルダ名を取得する
            String? inputCSVFileFolderName
                = System.IO.Path.GetDirectoryName(_CSVFilePath);
            if(inputCSVFileFolderName == null)
            {
                Console.WriteLine("Error occured on input CSV file directory acquisition");
                return;
            }

            //計算結果をCSVファイルとして保存する
            SaveCalculationResultLib svClcltnRsLib = new SaveCalculationResultLib();
            result = svClcltnRsLib.Save(inputCSVFileFolderName, mdznAdFlwRtLib);

            //計算終了を通知する
            Console.WriteLine("Calculation Done!");
        }
    }
}