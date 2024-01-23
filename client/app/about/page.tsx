"use client";

import { useEffect, useState } from "react";

type Props = {};

type Member = {
  id: number;
  name: string;
  // Add other member properties as needed
};

const Members = (props: Props) => {
  const [members, setMembers] = useState<Member[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch("/api/members/");
        let data = await response.json();
        setMembers(data.members);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <main>
      {members.map((member: Member) => (
        <li key={member.id} className="py-4">
          <p className="font-semibold">{member.id}</p>
          <p className="font-semibold">{member.name}</p>
        </li>
      ))}
    </main>
  );
};

export default Members;
