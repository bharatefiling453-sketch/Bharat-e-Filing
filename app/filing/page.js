import Navbar from "@/components/Navbar";
import FilingDashboard from "@/components/FilingDashboard";
import Footer from "@/components/Footer";

export const metadata = {
  title: "Start Filing — BharateFiling",
  description: "Configure tax source documents, import AIS / TIS records, and compile the draft Income Tax JSON payload.",
};

export default function FilingPage() {
  return (
    <div className="min-h-screen flex flex-col justify-between bg-[#030712] text-foreground">
      <Navbar />
      <main className="flex-grow flex flex-col justify-center">
        <FilingDashboard />
      </main>
      <Footer />
    </div>
  );
}
