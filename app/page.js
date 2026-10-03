import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col justify-between bg-[#030712] text-foreground">
      <Navbar />
      <main className="flex-grow flex flex-col justify-center">
        <HeroSection />
      </main>
      <Footer />
    </div>
  );
}
