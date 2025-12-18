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

  // Adjusted radius to fit within 700px container
  const radiusBase = 100;
  const containerSize = 700;

  return (
    <div className="flex flex-col items-center gap-4 p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-4">The Thirty-Three Cosmograph</h1>
      <p className="text-center text-muted-foreground mb-6">
        Three concentric choirs of eleven: Seraphic (Law and Flame), Empyreal (Motion and Desire), and Chthonic (Depth and Memory). Each ring mirrors the others; the Ninth Rim sits at the center as the Mouth of Silence.
      </p>
      
      <div 
        className="relative flex items-center justify-center"
        style={{ 
          width: `${containerSize}px`, 
          height: `${containerSize}px`,
          minHeight: `${containerSize}px`
        }}
      >
        {patrons.map((choir, index) => {
          const radius = radiusBase + index * 100;
          const ringSize = radius * 2;
          
          return (
            <motion.div
              key={choir.order}
              className="absolute flex items-center justify-center"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.4 }}
            >
              {/* Ring container */}
              <div
                className="rounded-full border-2 flex items-center justify-center"
                style={{
                  width: `${ringSize}px`,
                  height: `${ringSize}px`,
                  borderColor: choir.color,
                  borderWidth: index === 0 ? '1px' : '1.5px'
                }}
              >
                {/* Choir name label - positioned at top of ring */}
                <div
                  className="absolute text-sm font-semibold text-center"
                  style={{
                    left: '50%',
                    top: `-${radius + 12}px`,
                    transform: 'translateX(-50%)',
                    color: choir.color,
                    width: '120px',
                    whiteSpace: 'nowrap'
                  }}
                >
                  {choir.order}
                </div>
                
                {/* Patron names arranged on ring */}
                {choir.patrons.map((p, i) => {
                  const angle = (i / choir.patrons.length) * 2 * Math.PI - Math.PI/2; // Start from top
                  const x = radius * Math.cos(angle);
                  const y = radius * Math.sin(angle);
                  return (
                    <div
                      key={p}
                      className="absolute text-xs font-medium text-center"
                      style={{
                        left: `calc(50% + ${x}px)`,
                        top: `calc(50% + ${y}px)`,
                        transform: 'translate(-50%, -50%)',
                        color: choir.color,
                        width: '100px',
                        lineHeight: '1.2'
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
        
        {/* Center element */}
        <motion.div
          className="absolute flex items-center justify-center"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 1.5 }}
        >
          <Card className="w-32 h-32 rounded-full shadow-2xl bg-black text-white flex items-center justify-center">
            <CardContent className="p-3 text-center">
              <p className="text-sm font-bold">The Ninth Rim</p>
              <p className="text-xs italic mt-1">Mouth of Silence</p>
            </CardContent>
          </Card>
        </motion.div>
      </div>
      
      <div className="text-sm text-center text-muted-foreground max-w-2xl mt-4">
        <p>Each ring contains eleven patrons representing cosmic principles. The center symbolizes the silent void from which all creation emerges and to which all returns.</p>
      </div>
    </div>
  );
}
