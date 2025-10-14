import React from "react";
import SpotlightCard from '../components/SpotlightCard/SpotlightCard'
import {
    SiC,
    SiCplusplus,
    SiPython,
    SiJavascript,
    SiPhp,
    SiMysql,
    SiKotlin,
    SiReact,
    SiNodedotjs,
    SiExpress,
    SiMongodb,
    SiTailwindcss,
    SiBootstrap,
    SiPandas,
    SiNumpy,
    SiScikitlearn,
    SiGit,
    SiPostman,
    SiJupyter,
    SiDocker,
    SiVercel,
    SiRender
} from "react-icons/si";

// From Font Awesome
import { FaJava } from "react-icons/fa";

// From VS Code icon pack
import { VscVscode } from "react-icons/vsc";

// Fallback for R
import { TbLetterR } from "react-icons/tb";

const iconMap = {
    C: SiC,
    "C++": SiCplusplus,
    Java: FaJava,
    Python: SiPython,
    JavaScript: SiJavascript,
    PHP: SiPhp,
    SQL: SiMysql,
    Kotlin: SiKotlin,
    R: TbLetterR,
    React: SiReact,
    "Node.js": SiNodedotjs,
    Express: SiExpress,
    MongoDB: SiMongodb,
    Tailwind: SiTailwindcss,
    Bootstrap: SiBootstrap,
    Pandas: SiPandas,
    NumPy: SiNumpy,
    Matplotlib: SiPython, // fallback
    "Scikit-learn": SiScikitlearn,
    Git: SiGit,
    "VS Code": VscVscode,
    Postman: SiPostman,
    Jupyter: SiJupyter,
    Docker: SiDocker,
    "MERN Stack": SiReact,
    Vercel: SiVercel,
    Render: SiRender,
};

const sections = [
    {
        idx: 0,
        title: "Frontend Tools",
        color: "#d4ebe0",
        items: [
            "React",
            "Tailwind"
        ],
        description:
            "These are the tools used to construct the frontend of this web application",
    },
    {
        idx: 1,
        title: "Backend Tools",
        color: "#d4ebe0",
        items: [
            "Node.js",
            "Express",
        ],
        description:
            "The backend of this web application was developed using the following frameworks.",
    },
    {
        idx: 2,
        title: "Machine Learing Tools",
        color: "#d4ebe0",
        items: ["Pandas", "NumPy", "Matplotlib", "Scikit-learn"],
        description: "The machine learing prediction algorithm was trained using the following libraries",
    },
    {
        idx: 3,
        title: "Hosting & Other Tools",
        color: "#d4ebe0",
        items: ["Git", "Docker", "Vercel", "Render"],
        description: "These are the tools used for hosting and other developmental processes.",
    },
];

const Technology = () => {

    return (
        <div className="max-w-full mx-auto px-4 py-12 bg-gradient-to-t from-[#d4ebe0] to-[#B2FFD6]">

            <div className="text-center mb-16">
                <h2 className="text-5xl font-bold text-gray-700 mb-4">
                    Tools & Frameworks
                </h2>
                <p className="text-gray-600 text-lg max-w-2xl mx-auto">
                    The following tools and frameworks were used in the development of this project.
                </p>
            </div>

            <section className="px-6 py-20 md:px-12 mt-[-50px]">
                <div className="grid grid-cols-1 gap-8 mx-auto max-w-6xl w-[800px] max-h-[800px] sm:grid-cols-2">
                    {sections.map(({ idx, title, color, items, description }) => (
                        <SpotlightCard
                            key={title}
                            className={`p-6 backdrop-blur custom-spotlight-card bg-[#0f3f72] border-[1px] border-defaultWhite/30
      ${idx === 0 ? 'rounded-tr-3xl rounded-bl-3xl' : ''}
      ${idx === 1 ? 'rounded-tl-3xl rounded-br-3xl' : ''}
      ${idx === 2 ? 'rounded-tl-3xl rounded-br-3xl' : ''}
      ${idx === 3 ? 'rounded-bl-3xl rounded-tr-3xl' : ''}`
                            }
                            spotlightColor={color}
                        >
                            <h3 className="mb-4 text-2xl font-semibold text-defaultWhite font-gilroyRegular">
                                {title}
                            </h3>

                            <h3 className="mb-4 text-sm font-base text-defaultWhite font-gilroyLight">
                                {description}
                            </h3>

                            <ul className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
                                {items.map((item, idx) => {
                                    const IconComponent = iconMap[item];

                                    return (
                                        <li
                                            key={idx}
                                            className="flex flex-col justify-center items-center w-16 h-16 transition-transform cursor-pointer group text-defaultWhite hover:scale-110"
                                        >
                                            {IconComponent ? (
                                                <div className="flex flex-col items-center justify-center w-full h-full text-center">
                                                    <div className="flex items-center justify-center mb-1">
                                                        <IconComponent className="w-8 h-8" />
                                                    </div>
                                                    <span className="text-xs opacity-0 transition-all duration-200 ease-in-out translate-y-1 group-hover:opacity-100 group-hover:translate-y-0 font-gilroyLight">
                                                        {item}
                                                    </span>
                                                </div>
                                            ) : (
                                                <div className="flex items-center justify-center w-full h-full">
                                                    <span className="text-sm text-center">{item}</span>
                                                </div>
                                            )}
                                        </li>
                                    );
                                })}
                            </ul>
                        </SpotlightCard>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default Technology;
