import { useEffect, useState } from "react";
import {
  CheckCircle,
  Loader2,
  Cpu,
  Download,
  Rocket,
} from "lucide-react";
import {
  checkSetup,
  installEngine,
  modelStatus,
} from "../services/api";
import { useNavigate } from "react-router-dom";

function Setup() {

  const navigate = useNavigate();

  const [status, setStatus] = useState("Checking AI Engine...");
  const [loading, setLoading] = useState(true);
  const [installing, setInstalling] = useState(false);
  const [step, setStep] = useState(0);

  useEffect(() => {

    check();

  }, []);

  const check = async () => {

    try {

      const response = await checkSetup();

      if (response.data.status === "ready") {

            navigate("/");

        }

      else if (
        response.data.status === "not_installed"
      ) {

        setLoading(false);

        setStatus("AI Engine is not installed.");

      }

      else if (
        response.data.status === "model_missing"
      ) {

        setLoading(false);

        setStatus("AI Model is missing.");

      }

      else {

        setLoading(false);

        setStatus(response.data.message);

      }

    } catch {

      setLoading(false);

      setStatus("Unable to check setup.");

    }

  };
    const handleInstall = async () => {
        try {
            setStep(1);
            setStatus(
                "Installing AI Engine...\nThis may take a few minutes."
            );
            setInstalling(true);
            
            setLoading(true);
            
            setStep(2);
            setStatus("Starting AI Engine...");
            const response = await installEngine();

                if (!response.data.success) {
                    throw new Error(response.data.message);
                }
            

            let ready = false;

            while (!ready) {

                try {

                    const response = await checkSetup();

                    if (
                         response.data.status === "ready" ||
                        response.data.status === "not_running" ||
                        response.data.status === "model_missing"
                    ) {

                        ready = true;
                        

                    } else {

                        await new Promise(resolve =>
                            setTimeout(resolve, 2000)
                        );

                    }

                } catch {

                    await new Promise(resolve =>
                        setTimeout(resolve, 2000)
                    );

                }

            }
            setStep(3);
            setStatus(
                "Downloading AI Model...\nPlease wait..."
            );
            let installed = false;

            while (!installed) {

                const response = await modelStatus();

                if (response.data.installed) {

                    installed = true;

                } else {

                    await new Promise(resolve =>
                        setTimeout(resolve, 3000)
                    );

                }

            }
            setStep(4);
            setStatus("Finalizing Setup...");

            await new Promise(resolve => setTimeout(resolve, 1000));

            setLoading(false);
            setStatus("Setup Complete ");
            setInstalling(false);

            setTimeout(() => {
                navigate("/");

            }, 1500);

        }

        catch (err) {
            setInstalling(false);
            setLoading(false);

            console.error(err);

            setStatus(
                err?.message || "Setup Failed"
            );
        }

    };

  return (

    <div className="min-h-screen app-bg flex items-center justify-center">


        <div className="card-bg rounded-3xl p-10 w-[560px] shadow-2xl">

            <div className="flex flex-col items-center">

                <div className="w-20 h-20 rounded-full bg-cyan-500/20 flex items-center justify-center">

                    <Cpu
                        size={40}
                        className={`text-cyan-400 ${
                            loading ? "animate-pulse" : ""
                        }`}
                    />

                </div>

                <h1 className="text-3xl font-bold mt-5 text-theme">

                    Preparing AXON

                </h1>

                <p className="text-theme opacity-70 mt-3 text-center whitespace-pre-line">

                                {status}
                                </p>
                <p className="text-xs opacity-50 mt-2 text-center">
                The first setup may take several minutes depending on your internet speed.
            </p>

            <div className="mt-8 h-2 rounded-full bg-white/10 overflow-hidden">
                <div
                    className="h-full bg-cyan-400 transition-all duration-500"
                    style={{
                        width: `${Math.min(step * 25, 100)}%`
                    }}
                />
            </div>

            <div className="mt-2 text-center text-xs opacity-60">
                {Math.min(step * 25, 100)}% Complete
            </div>

            </div>  
            <div className="mt-10 space-y-5">

                <Step
                    done={step >= 1}
                    active={step === 1}
                    icon={<Cpu size={18} />}
                    text="Installing AI Engine"
                />

                <Step
                    done={step >= 2}
                    active={step === 2}
                    icon={<Rocket size={18} />}
                    text="Starting AI Engine"
                />

                <Step
                    done={step >= 3}
                    active={step === 3}
                    icon={<Download size={18} />}
                    text="Downloading AI Model"
                />

                <Step
                    done={step >= 4}
                    active={step === 4}
                    icon={<CheckCircle size={18} />}
                    text="Finalizing Setup"
                />

            </div>

            {!loading &&
            (
                status === "AI Engine is not installed." ||
                status === "AI Model is missing."
            ) && (

                <button
                    onClick={handleInstall}
                    disabled={installing}
                    className="mt-10 w-full rounded-2xl bg-cyan-500 hover:bg-cyan-600 py-4 font-semibold transition"
                >
                    {installing ? (

                        <div className="flex items-center justify-center gap-2">

                            <Loader2
                                size={18}
                                className="animate-spin"
                            />

                            Installing...

                        </div>

                    ) : (

                        "Install AI Engine"

                    )}
                </button>

            )}


        

      </div>

    </div>

  );

}
function Step({ done, active, icon, text }) {

    return (

        <div className="flex items-center gap-4">

            <div className="w-6 flex justify-center">

                {done ? (
                    <CheckCircle className="text-green-400" size={20} />
                ) : active ? (
                    <Loader2 className="animate-spin text-cyan-400" size={20} />
                ) : (
                    icon
                )}

            </div>

            <span className="text-theme">{text}</span>

        </div>

    );

}
export default Setup;