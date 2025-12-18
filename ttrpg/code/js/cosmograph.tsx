import { Card, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";

export default function Cosmograph33() {
  const patrons = [
    {
      order: "Seraphic",
      color: "#FFD580",
      patrons: [
        "Inaea",
        "Oath of Flame",
        "Mykkiel",
        "Sacred Geometry",
        "Inquisitor Prime",
        "Gallows Bell",
        "Varnek Karn",
        "Confessor",
        "Silent Choir",
        "Witness",
        "Sealed Gate"
      ]
    },
    {
      order: "Empyreal",
      color: "#CFA0E9",
      patrons: [
        "Ikasha",
        "Raéyn",
        "Thrysos",
        "Mab",
        "Livaea",
        "Palinode",
        "Aveh",
        "Morag",
        "Grimmir",
        "Maelstraeus",
        "Traveler"
      ]
    },
    {
      order: "Chthonic",
      color: "#7F7F7F",
      patrons: [
        "Isoka",
        "Malachai",
        "Carrion King",
        "Nidhoggr",
        "Khemesh",
        "Clockwork Monad",
        "Pale Shepherd",
        "Vorthak",
        "The Ninth",
        "Mor’iraath",
        "Ninth Rim"
      ]
    }
  ];

  const radiusBase = 200;

  return (
    <div className="flex flex-col items-center gap-4 p-6">
      <h1 className="text-3xl font-bold text-center mb-4">The Thirty-Three Cosmograph</h1>
      <p className="text-center text-muted-foreground max-w-2xl mb-6">
        Three concentric choirs of eleven: Seraphic (Law and Flame), Empyreal (Motion and Desire), and Chthonic (Depth and Memory). Each ring mirrors the others; the Ninth Rim sits at the center as the Mouth of Silence.
      </p>
      <div className="relative w-[700px] h-[700px]">
        {patrons.map((choir, index) => {
          const radius = radiusBase + index * 100;
          return (
            <motion.div
              key={choir.order}
              className="absolute inset-0 flex items-center justify-center"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.4 }}
            >
              <div
                className="rounded-full border border-gray-400/40 flex items-center justify-center"
                style={{
                  width: `${radius * 2}px`,
                  height: `${radius * 2}px`,
                  borderColor: choir.color
                }}
              >
                <div className="absolute text-sm font-semibold" style={{ color: choir.color, top: `${50 + index * 5}px` }}>
                  {choir.order}
                </div>
                {choir.patrons.map((p, i) => {
                  const angle = (i / choir.patrons.length) * 2 * Math.PI;
                  const x = radius * Math.cos(angle);
                  const y = radius * Math.sin(angle);
                  return (
                    <div
                      key={p}
                      className="absolute text-xs font-medium text-center w-28"
                      style={{
                        left: `calc(50% + ${x}px - 56px)` ,
                        top: `calc(50% + ${y}px - 10px)` ,
                        color: choir.color
                      }}
                    >
                      {p}
                    </div>
                  );
                })}
              </div>
            </motion.div>
          );
        })}
        <motion.div
          className="absolute inset-0 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
        >
          <Card className="w-32 h-32 flex items-center justify-center rounded-full shadow-lg bg-black text-white text-center">
            <CardContent>
              <p className="text-sm font-bold">The Ninth Rim</p>
              <p className="text-xs italic">Mouth of Silence</p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
