import Image from "next/image";

export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-purple-200">
      <h1 className="text-4xl font-bold text-gray-800 shadow-lg p-8 rounded-lg bg-white bg-opacity-80">
        Hello World
      </h1>
    </div>
  );
}
